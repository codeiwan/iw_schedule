document.addEventListener("DOMContentLoaded", function () {
  const recordButton = document.getElementById('recordButton');
  const recordingModal = document.getElementById('recordingModal');
  const closeModal = document.getElementById('closeModal');
  const startRecordingButton = document.getElementById('startRecordingButton');
  const stopRecordingButton = document.getElementById('stopRecordingButton');
  const cancelRecordingButton = document.getElementById('cancelRecordingButton');
  const recordingStatus = document.getElementById('recordingStatus');

  // 모달 열기
  recordButton.addEventListener('click', async () => {
    try {
      await fetch('/cancel_record', { method: 'POST' }); // 혹시 남아있는 녹음 취소
    } catch (error) {
      console.error("초기화 중 오류 발생:", error);
    }
    // 버튼 및 상태 초기화
    recordingStatus.textContent = "🎤 대기 중...";
    recordingStatus.classList.remove("recording");

    startRecordingButton.disabled = false;
    stopRecordingButton.disabled = true;
    cancelRecordingButton.disabled = true;

    recordingModal.style.display = 'flex';
  });

  // X 버튼 클릭 시 cancel_record 실행 후 모달 닫기
  closeModal.addEventListener('click', async () => {
    try {
      await fetch('/cancel_record', { method: 'POST' });
    } catch (error) {
      console.error("녹음 취소 오류:", error);
    }
    recordingModal.style.display = 'none';
  });

  // 녹음 시작
  startRecordingButton.addEventListener('click', async () => {
    try {
      let response = await fetch('/start_record', { method: 'POST' });
      let data = await response.json();

      recordingStatus.textContent = "🎤 녹음 중...";
      recordingStatus.classList.add("recording");

      startRecordingButton.disabled = true;
      stopRecordingButton.disabled = false;
      cancelRecordingButton.disabled = false;
    } catch (error) {
      console.error("녹음 시작 오류:", error);
    }
  });

  // 녹음 종료
  stopRecordingButton.addEventListener('click', async () => {
    try {
      let response = await fetch('/stop_record', { method: 'POST' });
      let data = await response.json();

      recordingStatus.textContent = "✅ 녹음 완료!";
      recordingStatus.classList.remove("recording");

      startRecordingButton.disabled = false;
      stopRecordingButton.disabled = true;
      cancelRecordingButton.disabled = true;

    } catch (error) {
      console.error("녹음 종료 오류:", error);
    }
  });

  // 녹음 취소
  cancelRecordingButton.addEventListener('click', async () => {
    try {
      await fetch('/cancel_record', { method: 'POST' });

      recordingStatus.textContent = "❌ 녹음 취소됨";
      recordingStatus.classList.remove("recording");

      startRecordingButton.disabled = false;
      stopRecordingButton.disabled = true;
      cancelRecordingButton.disabled = true;
    } catch (error) {
      console.error("녹음 취소 오류:", error);
    }
  });
});
