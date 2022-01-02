from transitions.extensions import GraphMachine

from utils import send_text_message

"""
text = event.message.text
        return text.lower() == "go to state1"
"""

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    def is_going_to_ask(self, event):
        return True
    def on_enter_ask(self, event):
        print("entering ask")
        reply_token = event.reply_token
        send_text_message(reply_token, "How have you been?\na)good\nb)bad")
    def is_going_to_bad(self, event):
        text = event.message.text
        return text.lower() == "b"
    def on_enter_bad(self, event):
        print("entering bad")
        reply_token = event.reply_token
        send_text_message(reply_token, "What\'s troubling you?\na)friends\nb)the other half\nc)work\n\nj)none of the above(will tell a joke)")       
    def is_going_to_nothing(self, event):
        text = event.message.text
        if text.lower() == "a":
            reply_token = event.reply_token
            send_text_message(reply_token, "Keep going")
            return True

#-------------------------------------------
    def is_going_to_friend(self, event):
        text = event.message.text
        return text.lower() == "a"
    def on_enter_friend(self, event):
        print("entering friend")
        reply_token = event.reply_token
        send_text_message(reply_token, "What\'s the matter\na)having an argument\nb)he/she being a jerk/cunt\nj)none of the above(will tell a joke)")
    
    def is_going_to_love(self, event):
        text = event.message.text
        return text.lower() == "b"
    def on_enter_love(self, event):
        print("entering love")
        reply_token = event.reply_token
        send_text_message(reply_token, "What\'s the matter\na)having an argument\nb)fading relationship\nc)being single for too long Orz\nj)none of the above(will tell a joke)")
    def is_going_to_fade(self, event):
        text = event.message.text
        return text.lower() == "b"
    def on_enter_fade(self, event):
        print("entering fade")
        reply_token = event.reply_token
        send_text_message(reply_token, "Is there a third party?\na)yes\nb)no")
    def is_going_to_third(self, event):
        text = event.message.text
        return text.lower() == "a"
    def on_enter_third(self, event):
        print("entering third")
        reply_token = event.reply_token
        send_text_message(reply_token, "Maybe it\'s time to leave. Forcing oneself only leads to greater catastrophe. It is totally fine to realize you don\'t fit each other. Rest for a while then move on!")
        self.go_back()
    def is_going_to_nothird(self, event):
        text = event.message.text
        return text.lower() == "b"
    def on_enter_nothird(self, event):
        print("entering nothird")
        reply_token = event.reply_token
        send_text_message(reply_token, "Fortunatety, both of you still have faith in each other. Sometimes expressing yourselves or simply saying \"I love you\" is go to have tremendous effect. So, GOOD LUCK!!")
        self.go_back()
    def is_going_to_single(self, event):
        text = event.message.text
        return text.lower() == "c"
    def on_enter_single(self, event):
        print("entering single")
        reply_token = event.reply_token
        send_text_message(reply_token, "Your are not alone...\nHere is my IG:duke_alien(for girls only)")
        self.go_back()
    
    def is_going_to_work(self, event):
        text = event.message.text
        return text.lower() == "c"
    def on_enter_work(self, event):
        print("entering work")
        reply_token = event.reply_token
        send_text_message(reply_token, "What\'s the matter\na)failed to make a progress\nb)somebody being an asshole\n\nj)none of the above(will tell a joke)")
    def is_going_to_progress(self, event):
        text = event.message.text
        return text.lower() == "a"
    def on_enter_progress(self, event):
        print("entering progress")
        reply_token = event.reply_token
        send_text_message(reply_token, "Is it fixable?\na)yes\nb)no")
    
    def is_going_to_fixable(self, event):
        text = event.message.text
        return text.lower() == "a"
    def on_enter_fixable(self, event):
        print("entering fixable")
        reply_token = event.reply_token
        send_text_message(reply_token, "Then what are you waiting for, lazy ass")
        self.go_back()
    def is_going_to_notfixable(self, event):
        text = event.message.text
        return text.lower() == "b"
    def on_enter_notfixable(self, event):
        print("entering notfixable")
        reply_token = event.reply_token
        send_text_message(reply_token, "It\'s no use crying over spilled water. Remember this lesson, and prevent it from ever happening again is all that you can do right now. Cheer up!")
        self.go_back()
    
#----------------------------------------------pool
    def is_going_to_argument(self, event):
        text = event.message.text
        return text.lower() == "a"
    def on_enter_argument(self, event):
        print("entering argument")
        reply_token = event.reply_token
        send_text_message(reply_token, "How was the condition?\na)trivial\nb)severe\nj)complicated(tell a joke, hopefully you get better)")
    def is_going_to_trivial(self, event):
        text = event.message.text
        return text.lower() == "a"
    def on_enter_trivial(self, event):
        print("entering trivial")
        reply_token = event.reply_token
        send_text_message(reply_token, "It\'s always fine to have little argument. Just make sure you express how you truly feel, and don\'t take it personally")
        self.go_back()
    def is_going_to_severe(self, event):
        text = event.message.text
        return text.lower() == "b"
    def on_enter_severe(self, event):
        print("entering severe")
        reply_token = event.reply_token
        send_text_message(reply_token, "Nothing is worse than a irrational conflict. I suggest waiting until you all calm down before looking for another conversation")
        self.go_back()


    def is_going_to_jerk(self, event):
        text = event.message.text
        return text.lower() == "b"
    def on_enter_jerk(self, event):
        print("entering jerk")
        reply_token = event.reply_token
        send_text_message(reply_token, "More often than not, we all have to deal with some bastards. What matters is that you don\'t get affected from them, knowing all the surroundings is temporary. So, take a deep breath then move on!")
        self.go_back()
    def is_going_to_joke(self, event):
        text = event.message.text
        return text.lower() == "j"
    def on_enter_joke(self, event):
        print("entering joke")
        reply_token = event.reply_token
        import random
        i = random.randrange(0,3)
        j =["Why don\'t scientists trust atoms?\n\n\nBecause they make up everything.", "How do you drown a hipster?\n\n\nThrow him in the mainstream.","Which country has the most strippers?\n\n\nPoland"]
        send_text_message(reply_token, j[i])
        self.go_back()    
