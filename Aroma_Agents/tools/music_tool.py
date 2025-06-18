# Aroma_Agents/tools/music_tool.py

import requests
from pathlib import Path
import time
import os
from typing import List, Dict, Any, Optional

from Aroma_Agents.utils.config import SUNO_API_KEY

# 定义 API 地址
BASE_URL = "https://apibox.erweima.ai/api/v1"
GENERATE_URL = f"{BASE_URL}/generate"
# <<< 核心修正 1: 使用最终正确的状态查询 URL >>>
STATUS_URL = f"{BASE_URL}/generate/record-info"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {SUNO_API_KEY}"
}

# --- 工具 1: 提交任务 (无需修改) ---
def submit_music_generation_task(lyrics: str, title: str) -> str:
    """
    Submits a music generation task to the Suno API and immediately returns a task ID.
    """
    if not SUNO_API_KEY:
        raise RuntimeError("SUNO_API_KEY not found in config.")

    print(f"🎵 Submitting music generation task for title: '{title}'...")
    payload = {
        "prompt": lyrics,
        "style": "emotional, healing song with feeling",
        "title": title,
        "customMode": True,
        "instrumental": False,
        "model": "V3_5",
        "callBackUrl": "https://webhook.site/" 
    }
    try:
        response = requests.post(GENERATE_URL, headers=HEADERS, json=payload, timeout=30)
        response.raise_for_status()
        task_data = response.json()
        if task_data.get("code") != 200 or not task_data.get("data") or "taskId" not in task_data.get("data"):
            print(f"❌ API did not return a valid task_id. Response: {task_data}")
            raise RuntimeError("Failed to submit generation task to Suno API.")
        task_id = task_data["data"]["taskId"]
        print(f"✅ Task submitted successfully. Use this Task ID for status checks: {task_id}")
        return task_id
    except requests.exceptions.RequestException as e:
        print(f"❌ Request to submit task failed: {e}")
        raise
    except (KeyError, TypeError) as e:
        print(f"❌ Failed to parse task_id from response. Response was: {task_data}. Error: {e}")
        raise

# --- 工具 2: 检查任务状态 (已根据新的 API 响应重写) ---
def check_music_generation_status(task_id: str) -> Dict[str, Any]:
    """
    Checks the status of a previously submitted task using the /generate/record-info endpoint
    and parses its specific JSON structure.
    """
    if not SUNO_API_KEY:
        raise RuntimeError("SUNO_API_KEY not found in config.")

    print(f"🕒 Checking status for Task ID: {task_id}...")
    
    try:
        status_response = requests.get(
            STATUS_URL, 
            headers=HEADERS, 
            params={"taskId": task_id}, 
            timeout=30
        )
        status_response.raise_for_status()
        response_data = status_response.json()

        if response_data.get("code") != 200:
            return {"status": "failed", "message": response_data.get("msg", "API returned a non-200 code."), "audio_urls": None}

        data_block = response_data.get("data")
        if not data_block or not isinstance(data_block, dict):
            return {"status": "processing", "message": "Task data block not yet available. Still processing.", "audio_urls": None}

        status = data_block.get("status")

        if status == "SUCCESS":
            # <<< 核心修正 2: 解析新的、嵌套的 JSON 结构 >>>
            suno_data_list = data_block.get("response", {}).get("sunoData", [])
            audio_urls = [item.get("audioUrl") for item in suno_data_list if item.get("audioUrl")] # 注意是 'audioUrl'
            
            if not audio_urls:
                 return {"status": "failed", "message": "Task status is SUCCESS, but no audio URLs were found in the response.", "audio_urls": None}

            print(f"✅ Task {task_id} is completed. Found {len(audio_urls)} audio file(s).")
            return {"status": "completed", "message": "Task completed successfully.", "audio_urls": audio_urls}
        
        elif status == "FAILED":
            error_detail = data_block.get("errorMessage", "Unknown server error.")
            print(f"❌ Task {task_id} has failed. Reason: {error_detail}")
            return {"status": "failed", "message": error_detail, "audio_urls": None}
        
        else: # Status is "PROCESSING", "PENDING", or something else
            print(f"⏳ Task {task_id} is still processing. Current API status: '{status}'.")
            return {"status": "processing", "message": f"Current status: '{status}'. Please check again later.", "audio_urls": None}

    except requests.exceptions.RequestException as e:
        print(f"❌ Polling request failed for Task ID {task_id}: {e}")
        return {"status": "error", "message": f"Network request failed: {e}", "audio_urls": None}

# --- 工具 3: 下载文件 (无需修改) ---
def download_music_files(audio_urls: List[str], base_filename: str) -> List[str]:
    # This function is already correct and does not need changes.
    output_dir = Path("music_outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    saved_files = []
    if not audio_urls:
        print("⚠️ No audio URLs provided to download.")
        return []

    print(f"⬇️ Starting download of {len(audio_urls)} file(s)...")
    for index, audio_url in enumerate(audio_urls):
        file_suffix = f"_{index + 1}" if len(audio_urls) > 1 else ""
        output_path = output_dir / f"{base_filename}{file_suffix}.mp3"
        print(f"🔗 Downloading '{output_path.name}' from: {audio_url[:70]}...")
        try:
            audio_response = requests.get(audio_url, timeout=120)
            audio_response.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(audio_response.content)
            print(f"✅ Music saved to: {output_path}")
            saved_files.append(str(output_path))
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Failed to download audio file from {audio_url}: {e}")
            continue
    if not saved_files:
        print("❌ Failed to download any of the generated audio files.")
    print("\n🎉 Download task finished!")
    return saved_files

# --- 编排器 (无需修改) ---
def create_and_generate_music(lyrics: str, filename: str) -> str:
    # This orchestrator calls the updated check_music_generation_status
    # and requires no changes itself.
    try:
        print(f"Orchestrator: Kicking off the music generation process for '{filename}'...")
        task_id = submit_music_generation_task(lyrics=lyrics, title=filename)
    except RuntimeError as e:
        error_message = f"Orchestrator ERROR: Could not start the process. {e}"
        print(error_message)
        return error_message

    print("Orchestrator: Waiting 2 seconds for the task to register on the server...")
    time.sleep(2)

    max_retries = 60
    wait_seconds = 10
    final_status = None

    print(f"Orchestrator: Starting to poll for task {task_id}. This may take several minutes...")
    for i in range(max_retries):
        if i > 0:
            time.sleep(wait_seconds)
        
        status_result = check_music_generation_status(task_id)
        current_status = status_result.get('status', 'unknown')
        
        if current_status == 'completed':
            final_status = status_result
            break
        elif current_status in ['failed', 'error']:
            final_status = status_result
            print(f"Orchestrator: Stopping polling due to failure or error: {status_result['message']}")
            break
        
        if i > 0 and (i * wait_seconds) % 30 == 0:
            print(f"Orchestrator: Still waiting for music generation... ({(i * wait_seconds) + 2} seconds elapsed)")

    if final_status and final_status['status'] == 'completed':
        audio_urls = final_status.get('audio_urls', [])
        if audio_urls:
            saved_files = download_music_files(audio_urls=audio_urls, base_filename=filename)
            if saved_files:
                result_message = f"Successfully generated and saved {len(saved_files)} song(s). Paths: {', '.join(saved_files)}"
                print(f"Orchestrator: {result_message}")
                return result_message
            else:
                return "Orchestrator ERROR: Task completed, but failed to download any files."
        else:
            return "Orchestrator ERROR: Task completed, but no audio URLs were found."
    elif final_status:
        return f"Orchestrator ERROR: Process failed. Final status: {final_status['status']}. Reason: {final_status['message']}"
    else:
        return f"Orchestrator ERROR: Polling timed out after {(max_retries * wait_seconds) / 60:.0f} minutes. The task took too long."