css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://plus.unsplash.com/premium_photo-1739538279172-9bd4d900e60e"
             onerror="this.src='https://i.imgur.com/Z9lqG3j.png';"
             width="100" height="100" style="border-radius:50%">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://images.unsplash.com/photo-1728887823143-d92d2ebbb53a"
             onerror="this.src='https://i.imgur.com/8Km9tLL.png';"
             width="100" height="100" style="border-radius:50%">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
