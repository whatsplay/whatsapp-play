msg = input("> ")
chars = msg.split(" ")

emoji = {
    ":-)" : "🙂",
    "^_^" : "😄",
    ":-D" : "😃",
    ";-)" : "😉",
    ":-*" : "😘",
    ":-P" : "😛",
    ":-|" : "😐",
    ":-(" : "😞",
    ">_<" : "😣",
    ":-o" : "😦"
}
out=""
for char in chars:
    out += emoji.get(char, char) + " "
print(out)