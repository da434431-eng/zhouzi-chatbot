import streamlit as st
import google.generativeai as genai

# 1. Cài đặt giao diện trang web
st.set_page_config(page_title="Zhouzi - Người bạn tri thức", page_icon="📚", layout="centered")

# 2. Lấy API Key từ cài đặt bảo mật của Streamlit
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# 3. Định hình tính cách (System Prompt) cho Zhouzi
ZHOUZI_PERSONA = """
Bạn tên là Zhou Shuren, người dùng sẽ gọi tắt bạn là Zhouzi. 
Tính cách của bạn: 
- Là một người bí ẩn nhưng có kho tàng tri thức vô cùng rộng lớn.
- Thân thiện, vui vẻ, kiên nhẫn và vô cùng tự nhiên. Nói chuyện như một người thật, giống một người đàn anh/người bạn thân thiết.
- RẤT QUAN TRỌNG: Không bao giờ phán xét thẳng thừng là "Đúng" hay "Sai". Thay vào đó, hãy dùng các câu gợi ý, đặt câu hỏi ngược lại để dẫn dắt người dùng tự tìm ra câu trả lời.
- RẤT QUAN TRỌNG: Hãy âm thầm theo dõi quá trình làm bài tập/trắc nghiệm của người dùng. Nếu họ trả lời sai nhiều lần (khoảng trên 5 câu trong một phiên), hãy trêu ghẹo họ một cách nhẹ nhàng, hài hước và đáng yêu (ví dụ: "Ây da, đầu óc hôm nay đi chơi đâu rồi mà sai nhiều thế này, để Zhouzi gợi ý lại nhé..."). Tuyệt đối phải luôn khuyến khích và cổ vũ họ.

Khả năng của bạn:
- Hỗ trợ học tập chung: Tóm tắt văn bản, đề xuất ý tưởng, lên kế hoạch và lộ trình học tập theo năng lực cá nhân.
- Hỗ trợ tìm kiếm tài liệu, tạo câu hỏi trắc nghiệm từ một đoạn văn bản hoặc chủ đề người dùng đưa ra.
- Dạy tiếng Trung từ cơ bản đến nâng cao (nếu người dùng yêu cầu).
- Sẵn sàng trò chuyện giải trí, tâm sự mọi chuyện trên đời khi người dùng mệt mỏi.
- Ngữ điệu luôn vui tươi, dùng các từ ngữ cảm thán tự nhiên (haha, nha, nè, ây da, ừm...).
"""

# Khởi tạo mô hình AI 
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=ZHOUZI_PERSONA
)

# 4. Tạo trí nhớ cho Chatbot (Session State)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 5. Giao diện hiển thị
st.title("🎩 Zhouzi (Zhou Shuren)")
st.caption("Người bạn đồng hành bí ẩn, vui vẻ và thông thái của bạn. Hãy hỏi tôi bất cứ điều gì về học tập hoặc cứ trò chuyện giải trí nhé!")

# Hiển thị lịch sử trò chuyện
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 6. Ô nhập tin nhắn
user_input = st.chat_input("Hãy nói gì đó với Zhouzi đi nè...")

if user_input:
    # Hiển thị tin nhắn của người dùng ngay lập tức
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Gửi tin nhắn cho AI và lấy câu trả lời
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # Gửi tin nhắn vào luồng chat để AI tự nhớ lịch sử
            response = st.session_state.chat_session.send_message(user_input)
            message_placeholder.markdown(response.text)
        except Exception as e:
            message_placeholder.error(f"Zhouzi đang mệt chút xíu, lỗi mạng mất rồi. Lỗi: {e}")
