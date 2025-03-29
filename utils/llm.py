import json
import datetime

def generate_schedule_response(client, user_message):
    today = datetime.date.today().isoformat()

    prompt = f"""
    You are a very capable time management secretary.

    You will analyze Korean sentences considering the context of the message and accurately extract the speaker's appointment time and content and return only JSON objects.
    Today's date is {today}. And you have to accurately figure out today's date and the date to carry out the schedule considering the context of the speaker's message and return it in the form of "1990-01-01".
    You should also summarize the features of the schedule, set the title, return it in Korean, and provide it as a value of "title."
    And you should provide the details as the value of "content."
    DO NOT return any explanation or description — only a JSON object in the following structure:

    {{
        "date": "YYYY-MM-DD",
        "title": "일정 제목",
        "content": "일정 상세 내용"
    }}

    Guidelines:
    - Today's standard is {today}.
    - Considering today's date and the speaker's message, the speaker's schedule should be accurately extracted.
    - 
    
    Text: "{user_message}"
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ],
        response_format={"type": "json_object"},
        max_tokens=150,
        temperature=0.3,
    )
    response_data = response.choices[0].message.content
        
    return json.loads(response_data)

    '''
    try:
        emotion_scores = json.loads(response.choices[0].message.content)
        required_keys = ["Joy", "Sadness", "Surprise", "Anger", "Fear", "Lovely", "None"]
        if not all(key in emotion_scores for key in required_keys):
            raise ValueError("Missing required emotion keys")

        # 소수점 정제 (혹시 Generator가 float을 int로 주는 경우)
        for key in required_keys:
            emotion_scores[key] = round(float(emotion_scores[key]), 3)

        return emotion_scores

    except json.JSONDecodeError:
        print("[응답에서 JSON 파싱 오류 발생] 응답 내용:", response.choices[0].message.content)

    except Exception as e:
        print(f"[예외 발생] {e}")

    # 실패 시 기본값 반환
    return {key: 0.0 for key in ["Joy", "Sadness", "Surprise", "Anger", "Fear", "Lovely", "None"]}'
    '''
