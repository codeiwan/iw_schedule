document.addEventListener("DOMContentLoaded", function () {
  const recordButton = document.getElementById('recordButton');
  const recordingModal = document.getElementById('recordingModal');
  const closeModal = document.getElementById('closeModal');
  const startRecordingButton = document.getElementById('startRecordingButton');
  const stopRecordingButton = document.getElementById('stopRecordingButton');
  const cancelRecordingButton = document.getElementById('cancelRecordingButton');
  const analyzeRecordingButton = document.getElementById('analyzeRecordingButton'); // 분석 버튼
  const recordingStatus = document.getElementById('recordingStatus');
  const sttResult = document.getElementById('sttResult'); // STT 결과
  
  const viewScheduleButton = document.getElementById("viewScheduleButton");
  const addScheduleButton = document.getElementById('addScheduleButton');
  const username = viewScheduleButton.getAttribute("data-username");
  const addScheduleModal = document.getElementById('addScheduleModal');
  const closeAddScheduleModal = document.getElementById('closeAddScheduleModal');
  const addScheduleForm = document.getElementById('addScheduleForm');

  // 모달 열기
  recordButton.addEventListener('click', async () => {
    try {
      await fetch('/cancel_record', { method: 'POST' }); // 혹시 남아있는 녹음 취소
    } catch (error) {
      console.error("초기화 중 오류 발생:", error);
    }
    // 버튼 및 상태 초기화
    recordingStatus.textContent = "대기 중...";
    recordingStatus.classList.remove("recording");
    sttResult.textContent = ""; // 이전 STT 결과 초기화

    startRecordingButton.disabled = false;
    stopRecordingButton.disabled = true;
    cancelRecordingButton.disabled = true;
    analyzeRecordingButton.disabled = true; // 시작 시에는 분석 비활성화

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

      recordingStatus.textContent = "녹음 중...";
      recordingStatus.classList.add("recording");
      
      // STT 결과를 빈 상태로 설정
    sttResult.textContent = "";
    
      startRecordingButton.disabled = true;
      stopRecordingButton.disabled = false;
      cancelRecordingButton.disabled = false;
      analyzeRecordingButton.disabled = true; // 녹음 중에는 분석 비활성화
    } catch (error) {
      console.error("녹음 시작 오류:", error);
    }
  });

  // 녹음 종료
  stopRecordingButton.addEventListener('click', async () => {
    try {
      let response = await fetch('/stop_record', { method: 'POST' });
      let data = await response.json();

      recordingStatus.textContent = "녹음 완료!";
      recordingStatus.classList.remove("recording");

      startRecordingButton.disabled = false;
      stopRecordingButton.disabled = true;
      cancelRecordingButton.disabled = true;
      
      // 분석 버튼 활성화 및 스타일 변경
      analyzeRecordingButton.disabled = false;
      analyzeRecordingButton.classList.add("active");
      console.log("분석 버튼 활성화됨");

    } catch (error) {
      console.error("녹음 종료 오류:", error);
    }
  });

  // 녹음 취소
  cancelRecordingButton.addEventListener('click', async () => {
    try {
      await fetch('/cancel_record', { method: 'POST' });

      recordingStatus.textContent = "녹음 취소됨";
      recordingStatus.classList.remove("recording");

      startRecordingButton.disabled = false;
      stopRecordingButton.disabled = true;
      cancelRecordingButton.disabled = true;
      
      // 분석 버튼 비활성화 및 스타일 제거
      analyzeRecordingButton.disabled = true;
      analyzeRecordingButton.classList.remove("active");
    } catch (error) {
      console.error("녹음 취소 오류:", error);
    }
  });

  // STT 분석 요청
  analyzeRecordingButton.addEventListener('click', async () => {
    try {
      const response = await fetch('/stt', { method: 'POST' });
      const data = await response.json();
      sttResult.textContent = `분석 결과: ${data.text}`;
    } catch (error) {
      console.error("STT 분석 오류", error);
      sttResult.textContent = "분석 실패!";
    }
  });

  // 일정 보기 버튼 클릭 시, 사용자 일정 페이지로 이동
  viewScheduleButton.addEventListener("click", function() {
    window.location.href = `/schedule/${username}`;  // 해당 사용자 일정 페이지로 이동
  });

  // 일정 추가 모달 열기
  addScheduleButton.addEventListener('click', () => {
    addScheduleModal.style.display = 'flex';
  });

  // X 버튼 클릭 시 모달 닫기
  closeAddScheduleModal.addEventListener('click', () => {
    addScheduleModal.style.display = 'none';
  });

  // 일정 추가 모달에 기능 추가
  addScheduleForm.addEventListener('submit', async (event) => {
    event.preventDefault(); // 기본 제출 동작 방지

    const date = document.getElementById('scheduleDate').value;
    const title = document.getElementById('scheduleTitle').value;
    const content = document.getElementById('scheduleContent').value;

    const requestData = {
        username: username,
        date: date,
        title: title,
        content: content
    };

    try {
        const response = await fetch('/add_schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            throw new Error('네트워크 응답이 좋지 않습니다.');
        }

        const result = await response.json();
        console.log('일정 추가 결과:', result);
        // 모달 닫기 및 폼 초기화
        addScheduleModal.style.display = 'none';
        addScheduleForm.reset();
    } catch (error) {
        console.error('일정 추가 중 오류 발생:', error);
    }
});

  // 달력 기능 추가
  const today = new Date();
  let currentMonth = today.getMonth();
  let currentYear = today.getFullYear();

  const monthYear = document.getElementById("month-year");
  const calendarDays = document.getElementById("calendar-days");

  const months = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"];

  function showCalendar(month, year) {
    const firstDay = new Date(year, month).getDay();  // 월의 첫 번째 날의 요일 (0: 일요일, 6: 토요일)
    const daysInMonth = 32 - new Date(year, month, 32).getDate();  // 해당 월의 총 일수

    calendarDays.innerHTML = "";

    // 제목 설정 (YYYY년 MM월)
    monthYear.textContent = `${year}년 ${months[month]}`;

    let date = 1;
    for (let i = 0; i < 6; i++) {
      const row = document.createElement("tr");

      for (let j = 0; j < 7; j++) {
        if (i === 0 && j < firstDay) {
          // 첫 번째 주에서 빈 칸 추가
          const cell = document.createElement("td");
          cell.innerHTML = "";
          row.appendChild(cell);
        } else if (date > daysInMonth) {
          // 해당 월의 마지막 날짜를 넘으면 중단
          break;
        } else {
          // 날짜 채우기
          const cell = document.createElement("td");
          cell.textContent = date;

          // 오늘 날짜 강조
          if (date === today.getDate() && year === today.getFullYear() && month === today.getMonth()) {
            cell.classList.add("bg-warning");
          }

          row.appendChild(cell);
          date++;
        }
      }

      calendarDays.appendChild(row);
    }
  }

  document.getElementById("prev-month").addEventListener("click", function() {
    currentYear = (currentMonth === 0) ? currentYear - 1 : currentYear;
    currentMonth = (currentMonth === 0) ? 11 : currentMonth - 1;
    showCalendar(currentMonth, currentYear);
  });

  document.getElementById("next-month").addEventListener("click", function() {
    currentYear = (currentMonth === 11) ? currentYear + 1 : currentYear;
    currentMonth = (currentMonth + 1) % 12;
    showCalendar(currentMonth, currentYear);
  });

  // 페이지 로드 시 달력 표시
  showCalendar(currentMonth, currentYear);
});
