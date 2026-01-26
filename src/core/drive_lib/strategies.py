import os
import io
from abc import ABC, abstractmethod

class DriveStrategy(ABC):
    """Abstract base class for file drive strategies (save/load/download)."""
    @abstractmethod
    def save(self, file_obj: io.StringIO, filename: str) -> None:
        """
        Saves the content of a file object to the storage.

        Args:
            file_obj (io.StringIO): The file object containing content to save.
            filename (str): The name of the file to save.
        """
        pass

    @abstractmethod
    def load(self, filename: str) -> str:
        """
        Loads the content of a file as a string.

        Args:
            filename (str): The name of the file to load.

        Returns:
            str: The content of the file.
        """
        pass

    @abstractmethod
    def download(self, filename: str, save_path: str) -> None:
        """
        Downloads a file to a local path.

        Args:
            filename (str): The name of the file to download.
            save_path (str): The local path where the file should be saved.
        """
        pass

class LocalFileStrategy(DriveStrategy):
    """Strategy for saving and loading files to/from the local filesystem."""
    def __init__(self, base_path: str = ""):
        """
        Initializes the local file strategy.

        Args:
            base_path (str): The base directory for file operations. Defaults to current directory.
        """
        self.base_path = base_path

    def save(self, file_obj: io.StringIO, filename: str) -> None:
        """Saves content to a local file."""
        target_path = os.path.join(self.base_path, filename)
        directory = os.path.dirname(target_path)
        if directory:
            # 디렉토리가 존재하지 않으면 생성
            os.makedirs(directory, exist_ok=True)
            
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(file_obj.getvalue())

    def load(self, filename: str) -> str:
        """Reads content from a local file."""
        target_path = os.path.join(self.base_path, filename)
        with open(target_path, "r", encoding="utf-8") as f:
            return f.read()

    def download(self, filename: str, save_path: str) -> None:
        """Copies a local file to another location."""
        import shutil
        source_path = os.path.join(self.base_path, filename)
        if os.path.dirname(save_path):
            # 저장할 경로의 상위 디렉토리가 없으면 생성
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
        shutil.copy(source_path, save_path)

class GoogleDriveStrategy(DriveStrategy):
    """
    Strategy for saving and loading files to/from Google Drive.
    Requires 'google-api-python-client'.
    """
    def __init__(self, drive_service=None, folder_id: str = None, credentials_path: str = None):
        """
        Initializes the Google Drive strategy.

        Args:
            drive_service: Authenticated Google Drive service object.
            folder_id (str, optional): The ID of the folder to save/load files.
            credentials_path (str, optional): Path to the service account JSON key file.
        """
        self.folder_id = folder_id
        
        if drive_service:
            self.service = drive_service
        elif credentials_path:
            self.service = self._authenticate(credentials_path)
        else:
            raise ValueError("Either 'drive_service' object or 'credentials_path' must be provided.")
    
    def _authenticate(self, credentials_path: str):
        """
        Authenticates using a service account JSON file.

        Args:
            credentials_path (str): Path to the service account JSON file.

        Returns:
            Resource: Authenticated Google Drive service resource.
        """
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
        except ImportError:
            # 인증 관련 라이브러리 동적 설치
            from ..py_lib.python_lib import install_lib
            install_lib("google.oauth2", "google-auth")
            install_lib("googleapiclient", "google-api-python-client")
            from google.oauth2 import service_account
            from googleapiclient.discovery import build

        # Google Drive API 접근 권한 범위 설정
        SCOPES = ['https://www.googleapis.com/auth/drive']
        # 서비스 계정 키 파일을 로드하여 자격 증명 생성
        creds = service_account.Credentials.from_service_account_file(
            credentials_path, scopes=SCOPES
        )
        return build('drive', 'v3', credentials=creds)

    def save(self, file_obj: io.StringIO, filename: str) -> None:
        """Uploads a file to Google Drive."""
        try:
            from googleapiclient.http import MediaIoBaseUpload
        except ImportError:
            from ..py_lib.python_lib import install_lib
            install_lib("googleapiclient", "google-api-python-client")
            from googleapiclient.http import MediaIoBaseUpload

        # 문자열 데이터를 API 전송을 위해 바이너리 스트림으로 변환
        binary_stream = io.BytesIO(file_obj.getvalue().encode('utf-8'))
        file_metadata = {'name': filename}
        if self.folder_id:
            # 특정 폴더에 저장하기 위해 부모 ID 지정
            file_metadata['parents'] = [self.folder_id]
            
        # 대용량 파일도 처리 가능한 재개 가능한 업로드(Resumable Upload) 방식 사용
        media = MediaIoBaseUpload(binary_stream, mimetype='application/octet-stream', resumable=True)
        self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    def _find_file_id(self, filename: str) -> str:
        """Finds the file ID for a given filename in the specified folder."""
        # 파일명과 일치하고 휴지통에 없는 파일 검색 쿼리
        query = f"name = '{filename}' and trashed = false"
        if self.folder_id:
            # 지정된 폴더 내에서만 검색하도록 조건 추가
            query += f" and '{self.folder_id}' in parents"
            
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get('files', [])

        if not files:
            raise FileNotFoundError(f"File '{filename}' not found in Google Drive.")
        return files[0]['id']

    def _download_stream(self, file_id: str, output_stream: io.IOBase) -> None:
        """Downloads file content from Google Drive to a stream."""
        try:
            from googleapiclient.http import MediaIoBaseDownload
        except ImportError:
            from ..py_lib.python_lib import install_lib
            install_lib("googleapiclient", "google-api-python-client")
            from googleapiclient.http import MediaIoBaseDownload

        # 파일 미디어 다운로드 요청 생성
        request = self.service.files().get_media(fileId=file_id)
        downloader = MediaIoBaseDownload(output_stream, request)
        
        done = False
        while done is False:
            # 파일을 청크(Chunk) 단위로 나누어 다운로드
            status, done = downloader.next_chunk()

    def load(self, filename: str) -> str:
        """Downloads a file from Google Drive and returns its content as a string."""
        file_id = self._find_file_id(filename)
        file_content = io.BytesIO()
        self._download_stream(file_id, file_content)
        return file_content.getvalue().decode('utf-8')

    def download(self, filename: str, save_path: str) -> None:
        """Downloads a file from Google Drive to a local path."""
        file_id = self._find_file_id(filename)
        if os.path.dirname(save_path):
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            self._download_stream(file_id, f)

class DiscordStrategy(DriveStrategy):
    """
    Storage strategy for uploading/downloading files to/from a Discord Channel.
    'save' uses Bot Token (Searchable).
    'save_webhook' uses Webhook URL (Not searchable).
    'load' requires Bot Token and Channel ID to search message history.
    """
    def __init__(self, webhook_url: str = None, bot_token: str = None, channel_id: str = None):
        """
        Initializes the Discord strategy.

        Args:
            webhook_url (str, optional): Discord Webhook URL for saving files.
            bot_token (str, optional): Discord Bot Token for saving/loading files.
            channel_id (str, optional): Discord Channel ID for saving/loading files.
        """
        self.webhook_url = webhook_url
        self.bot_token = bot_token
        self.channel_id = channel_id
        
        if not self.webhook_url and not (self.bot_token and self.channel_id):
            raise ValueError("DiscordStrategy requires either 'webhook_url' OR ('bot_token' and 'channel_id').")

    def save(self, file_obj: io.StringIO, filename: str) -> None:
        """
        Uploads a file to a Discord channel via Bot (Searchable).
        To use Webhook, use 'save_webhook' method.
        """
        if not self.bot_token or not self.channel_id:
            raise ValueError("Saving via Bot requires 'bot_token' and 'channel_id'.")

        file_content = file_obj.getvalue().encode('utf-8')
        self._save_via_bot(filename, file_content)

    def save_webhook(self, file_obj: io.StringIO, filename: str) -> None:
        """Uploads a file to a Discord channel via Webhook (Not searchable)."""
        if not self.webhook_url:
            raise ValueError("Saving via Webhook requires 'webhook_url'.")

        file_content = file_obj.getvalue().encode('utf-8')
        self._save_via_webhook(filename, file_content)
            
    def _save_via_webhook(self, filename: str, file_content: bytes) -> None:
        """Uploads a file using a Webhook URL."""
        import requests
        # Webhook으로 파일 전송 (multipart/form-data)
        files = [
            ('file', (filename, file_content, 'application/octet-stream'))
        ]
        response = requests.post(self.webhook_url, files=files)
        response.raise_for_status()

    def _save_via_bot(self, filename: str, file_content: bytes) -> None:
        """Uploads a file using a Bot Token."""
        import requests
        # 채널 메시지 생성 API 엔드포인트
        url = f"https://discord.com/api/v10/channels/{self.channel_id}/messages"
        # 봇 인증 헤더 추가 ('Bot ' 접두사 필수)
        headers = {"Authorization": f"Bot {self.bot_token}"}
        files = [
            ('file', (filename, file_content, 'application/octet-stream'))
        ]
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()

    def _fetch_recent_messages(self, limit: int = 100):
        """Fetches recent messages from the channel."""
        if not self.bot_token or not self.channel_id:
            raise ValueError("Loading from Discord requires 'bot_token' and 'channel_id'.")
            
        import requests
        headers = {"Authorization": f"Bot {self.bot_token}"}
        # 채널의 최근 메시지 목록 조회 (limit 파라미터로 개수 제한)
        url = f"https://discord.com/api/v10/channels/{self.channel_id}/messages?limit={limit}"
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def _find_attachment_url(self, filename: str) -> str:
        """Finds the attachment URL for a given filename in recent messages."""
        messages = self._fetch_recent_messages()
        for message in messages:
            # 메시지에 포함된 모든 첨부파일 확인
            for attachment in message.get('attachments', []):
                if attachment.get('filename') == filename:
                    return attachment.get('url')
        raise FileNotFoundError(f"File '{filename}' not found in the last 100 messages of the Discord channel.")

    def _download_content(self, url: str) -> bytes:
        """Downloads the content of an attachment from a URL."""
        import requests
        response = requests.get(url)
        response.raise_for_status()
        return response.content

    def load(self, filename: str) -> str:
        """Downloads a file from Discord and returns its content as a string."""
        url = self._find_attachment_url(filename)
        content = self._download_content(url)
        return content.decode('utf-8')

    def download(self, filename: str, save_path: str) -> None:
        """Downloads a file from Discord to a local path."""
        url = self._find_attachment_url(filename)
        content = self._download_content(url)
        
        if os.path.dirname(save_path):
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(content)

    def load_latest(self, n: int = 0) -> str:
        """
        Fetches the content of the n-th latest file from the Discord channel.
        
        Args:
            n (int): The index of the file to load (0 is the most recent).

        Returns:
            str: The content of the file.
        """
        messages = self._fetch_recent_messages()
        current_index = 0
        
        for message in messages:
            for attachment in message.get('attachments', []):
                # 최신순으로 n번째 파일인지 확인
                if current_index == n:
                    content = self._download_content(attachment.get('url'))
                    return content.decode('utf-8')
                current_index += 1
        
        raise FileNotFoundError(f"File at index {n} not found in the last 100 messages.")

class TelegramStrategy(DriveStrategy):
    """Storage strategy for uploading files to a Telegram Channel/Chat."""
    def __init__(self, bot_token: str, chat_id: str):
        """
        Initializes the Telegram strategy.

        Args:
            bot_token (str): Telegram Bot Token.
            chat_id (str): Telegram Chat ID.
        """
        self.bot_token = bot_token
        self.chat_id = chat_id

    def save(self, file_obj: io.StringIO, filename: str) -> None:
        """Uploads a file to a Telegram chat."""
        import requests
        # 텔레그램 봇 API의 문서 전송 엔드포인트
        url = f"https://api.telegram.org/bot{self.bot_token}/sendDocument"
        # 파일 데이터 준비 (파일명, 내용)
        files = {'document': (filename, file_obj.getvalue().encode('utf-8'))}
        # 채팅 ID를 폼 데이터로 함께 전송
        data = {'chat_id': self.chat_id}
        response = requests.post(url, files=files, data=data)
        response.raise_for_status()

    def load(self, filename: str) -> str:
        """Raises NotImplementedError as loading by filename is not supported."""
        raise NotImplementedError(
            "Loading files by filename is not supported in TelegramStrategy "
            "because the Telegram Bot API does not allow searching chat history."
        )

    def download(self, filename: str, save_path: str) -> None:
        """Raises NotImplementedError as downloading by filename is not supported."""
        raise NotImplementedError(
            "Downloading files by filename is not supported in TelegramStrategy "
            "because the Telegram Bot API does not allow searching chat history."
        )
