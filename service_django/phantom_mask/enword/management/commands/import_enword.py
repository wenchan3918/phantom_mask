import os
from string import ascii_lowercase

from django.core.management.base import BaseCommand

from enword.models import ENWord


# python manage.py import_data
class Command(BaseCommand):
    help = '英文單字匯入與搜尋'
    current = os.path.dirname(os.path.abspath(__file__))

    prefixs = [
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "", "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "", "",
        "",
        "",
        "",
        "", "",
        "",
        "",
        "",
        "",

    ]

    roots = [
        "ann",
        "audi",
        "bio",
        "cap",
        "ceive",
        "cip",
        "cept",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ]

    suffixs = set((
        "er",
        "or",
        "ar",
        "an",
        "ee",
        "ese",
        "ic",
        "ant",
        "ent",
        "ance",
        "ence",
        "ion",
        "ize",
        "en",
        "ary",
        "ory",
        "ful",
        "ous",
        "ious",
        "able",
        "ible",
        "al",
        "ial",
        "ic",
        "ical",
        "ish",
        "ive",
        "ative",
        "itive",
        "less",
        "ly",
        "ment",
        "ness",
        "ous",
        "ess",
        "ist",
        "ster",
        "age",
        "ance",
        "ence",
        "ancy",
        "ency",
        "dom",
        "hood",
        "ism",
        "ity",
        "ty",
        "logy",
        "ness",
        "ment",
        "ory",
        "ship",
        "tion",
        "ation",
        "sion",
        "ure",
        "ture",
        "fy",
        "ify",
        "ish",
        "ize",
        "ise",
        "le",
        "able",
        "ible",
        "al",
        "ant",
        "ent",
        "ary",
        "ate",
        "ful",
        "ical",
        "id",
        "ish",
        "ive",
        "like",
        "ous",
        "proof",
        "ward",
        "ward",
        "wise",
        "way",
        "ze",
        "ize",
        "logy",
    ))

    def handle(self, *args, **options):
        # self.import_data()
        # os.rmdir(f'{self.current}/suffix')

        self.count_suffix()
    def count_suffix(self):
        os.mkdir(f'{self.current}/suffix')
        for word in self.suffixs:
            self.count_endswith(words=[word], show_word=True)

    def suffix_foreach(self):
        for c1 in ascii_lowercase:
            for c2 in ascii_lowercase:
                self.count_endswith(words=[f'{c1}{c2}'], show_word=True)
                for c3 in ascii_lowercase:
                    self.count_endswith(words=[f'{c1}{c2}{c3}'], show_word=True)
                    for c4 in ascii_lowercase:
                        self.count_endswith(words=[f'{c1}{c2}{c3}{c4}'], show_word=True)

    def count_endswith(self, words, show_word=False):
        """
        1.ment 是接在動詞後面的名詞字尾，用來表示「行為」、「狀態」或「結果」。
        2.-ance 或 -ence 這個尾綴詞源於拉丁文，用來表示「動作」、「狀態」或「性質」，而 -ance 或 -ence 的個別使用時機呢？很抱歉，答案沒有人知道，只能用背的了。
        3. -ant 或 -ent 如果接在動詞之後，可以用來表示「執行某事物的人」，這樣就只需要背前面的動詞，就可以順便看懂這個動詞的執行者了。
        4.-er 或 -or 或 -ar 這三個皆在動詞後面的名詞字尾，用來表示「從事…的人」或「具備…的事物」，特別的是，帶有「貿易」性質的字，我們會將 -er 改成 -ier，在 w 後也會改寫成 -yer ，另外，or 會接在源自拉丁文的動詞之後。
        5.-ion 這個字堪稱是尾綴詞的霸主，使用頻率超級高，是一定要會的名詞字尾！常以 -tion、-sion、-ation、-tion 的形式出現，用以表示「行動」「狀態」「過程」和「行動」，以下的老師提供很多例子，讓你印象超深刻，一定要學起來！
        6.-ize 接在形容詞或名詞後動詞字尾，用來表示「使變成」或「使…受影響」的意思，幾乎所有的名詞和形容詞都可以因為這個尾綴詞而變成動詞。
        2. -en 當 -en 出現在字尾和字首時，皆可將形容詞或名詞變成動詞，用來表示「使…」
        1. -ary 或 -ory用來表示「與…相關」或是「像…」的形容詞字尾
        -ful 出現次數超級高的形容詞字尾，接在名詞後表示「有…特性」或「…的數量」，接在動詞時表示「易於…」，如果在形容詞之後，意思則不會有太大的改變。
        -ous 或  -ious 常接在動詞或名詞後的形容詞字尾，用來表示「充滿…」或「有…特性」
        -less 帶有否定意涵的形容詞字尾，如果接在名詞後面，表示「沒有…」但如果接在動詞後面，表示「無法…」或「不受…的影響」
        """

        for word in words:
            print(word)
            if os.path.isfile(f'{self.current}/suffix/{word}.yml'):
                continue

            results = []
            count = ENWord.objects.filter(en__endswith=word).count()
            results.append(f'{word} endswith: {count}')
            if count < 10:
                continue

            if show_word:
                for obj in ENWord.objects.filter(en__endswith=word).order_by('en'):
                    print(obj.en)
                    results.append(f"{obj.en}:")

                with open(f'{self.current}/suffix/{count}_{word}.yml', 'w') as f:
                    f.write('\n'.join(results))

            print(f'{word} endswith: {count}')

    def import_data(self):

        words = []
        with open(f'{self.current}/words_alpha.txt', 'r') as f:
            for word in f.readlines():
                word = word.strip()
                if len(word) > 0:
                    words.append(word)
        count = 0
        for word in words:
            # print(count, word)
            count += 1
            obj, created = ENWord.objects.get_or_create(en=word)
            print(f'{count} created: {created}, {obj.en}')
