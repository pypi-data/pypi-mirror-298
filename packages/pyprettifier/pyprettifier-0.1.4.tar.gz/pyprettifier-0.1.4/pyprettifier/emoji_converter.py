# pyprettifier/emoji_converter.py
from .logger import *
import requests

emoji_dict = {
    ":smile:": "😄",
    ":heart:": "❤️",
    ":thumbs_up:": "👍",
    ":cry:": "😢",
    ":laughing:": "😆",
    ":fire:": "🔥",
    ":clap:": "👏",
    ":sunglasses:": "😎",
    ":star:": "⭐",
    ":thinking:": "🤔",
    ":grinning:": "😀",
    ":winking:": "😉",
    ":blush:": "😊",
    ":angry:": "😠",
    ":astonished:": "😲",
    ":confused:": "😕",
    ":cool:": "😎",
    ":disappointed:": "😞",
    ":expressionless:": "😑",
    ":face_with_tears_of_joy:": "😂",
    ":fearful:": "😨",
    ":flushed:": "😳",
    ":hugging:": "🤗",
    ":kiss:": "😘",
    ":neutral_face:": "😐",
    ":pensive:": "😔",
    ":relieved:": "😌",
    ":sleeping:": "😴",
    ":sweat_smile:": "😅",
    ":unamused:": "😒",
    ":worried:": "😟",
    ":yum:": "😋",
    ":upside_down_face:": "🙃",
    ":poop:": "💩",
    ":rocket:": "🚀",
    ":raised_hands:": "🙌",
    ":wave:": "👋",
    ":ok_hand:": "👌",
    ":pray:": "🙏",
    ":muscle:": "💪",
    ":100:": "💯",
    ":celebrate:": "🎉",
    ":birthday:": "🎂",
    ":balloon:": "🎈",
    ":cake:": "🍰",
    ":coffee:": "☕",
    ":pizza:": "🍕",
    ":hamburger:": "🍔",
    ":beer:": "🍺",
    ":trophy:": "🏆",
    ":medal:": "🏅",
    ":soccer:": "⚽",
    ":basketball:": "🏀",
    ":checkered_flag:": "🏁",
    ":snowflake:": "❄️",
    ":sunny:": "☀️",
    ":umbrella:": "☂️",
    ":cloud:": "☁️",
    ":moon:": "🌙",
    ":earth:": "🌍",
    ":rainbow:": "🌈",
    ":lightning:": "⚡",
    ":star2:": "🌟",
    ":sparkles:": "✨",
    ":zap:": "⚡",
    ":red_heart:": "❤️",
    ":broken_heart:": "💔",
    ":skull:": "💀",
    ":ghost:": "👻",
    ":alien:": "👽",
    ":robot:": "🤖",
    ":pumpkin:": "🎃",
    ":snowman:": "⛄",
    ":christmas_tree:": "🎄",
    ":jack_o_lantern:": "🎃",
    ":crown:": "👑",
    ":ring:": "💍",
    ":diamond:": "💎",
    ":moneybag:": "💰",
    ":credit_card:": "💳",
    ":bank:": "🏦",
    ":airplane:": "✈️",
    ":train:": "🚂",
    ":car:": "🚗",
    ":bus:": "🚌",
    ":bicycle:": "🚲",
    ":police_car:": "🚓",
    ":fire_truck:": "🚒",
    ":ambulance:": "🚑",
    ":tractor:": "🚜",
    ":fuelpump:": "⛽",
    ":hourglass:": "⌛",
    ":watch:": "⌚",
    ":computer:": "💻",
    ":mobile_phone:": "📱",
    ":camera:": "📷",
    ":headphones:": "🎧",
    ":microphone:": "🎤",
    ":movie_camera:": "🎥",
    ":television:": "📺",
    ":video_game:": "🎮",
    ":satellite:": "🛰️",
    ":rocket:": "🚀",
    ":alien:": "👽"
}


class EmojiConverter:

    @log_function_call_external
    def __init__(self, update=True):
        if update:
            pass
            refine in the future, this is a test to get an html page with a full emoji list
            self.update_url = 'https://unicode.org/Public/emoji/1.0/emoji-data.txt'
            requests.get(self.update_url, timeout=2)


    @staticmethod
    def convert(emoji_name):
        """
        Converts an emoji name to the actual emoji character.
        
        :param emoji_name: Emoji name in the format ':emoji_name:'
        :return: Corresponding emoji character, or a message if not found
        """
        return emoji_dict.get(emoji_name, "Emoji not found")
    
    @staticmethod
    def replace_string_with_emoji(text):
        """
        Replaces all occurrences of :emoji_name: in the text with the corresponding emoji.
        
        :param text: String that may contain emoji names in the format ':emoji_name:'
        :return: String with emoji names replaced by actual emojis
        """
        for emoji_name in emoji_dict.keys():
            text = text.replace(emoji_name, emoji_dict[emoji_name])
        return text
    
    @staticmethod
    def replace_emojis_with_string(text):
        """
        Replaces all actual emoji characters in the text with their corresponding :emoji_name: tags.
        
        :param text: String that may contain actual emojis
        :return: String with emojis replaced by their :emoji_name: tags
        """
        reversed_emoji_dict = {v: k for k, v in emoji_dict.items()}
        
        for emoji_char, emoji_name in reversed_emoji_dict.items():
            text = text.replace(emoji_char, emoji_name)
        
        return text

    @staticmethod
    def replace_emojis_with_alternatives(text, replacements):
        """
        Replaces all emojis in the text with custom alternative replacements.
        
        :param text: String that may contain emojis
        :param replacements: A dictionary where the key is the emoji and the value is the replacement (text, emoji, or any other symbol).
        :return: String with emojis replaced by the provided alternatives
        """
        reversed_emoji_dict = {v: k for k, v in emoji_dict.items()}
        
        for emoji_char, emoji_name in reversed_emoji_dict.items():
            if emoji_char in replacements:
                text = text.replace(emoji_char, replacements[emoji_char])
        
        return text
    
    @staticmethod
    def remove_emojis(text):
        """
        Removes all emoji characters from the string, leaving only the non-emoji text.
        
        :param text: String that may contain emojis
        :return: String with all emojis removed
        """
        reversed_emoji_dict = {v: k for k, v in emoji_dict.items()}
        # Iterate through the emoji characters and remove them from the text
        for emoji_char in reversed_emoji_dict.keys():
            text = text.replace(emoji_char, '')
        return text

    def write_to_file(text, file_path):
        """
        Writes the given text to a specified file.
        
        :param text: The text to write
        :param file_path: The path of the file to write to
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)
            return True
        except Exception as e:
            return False  
