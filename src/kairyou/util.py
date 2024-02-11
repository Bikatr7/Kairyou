## built-in libraries
import enum
import typing
import os

##-------------------start-of-get_elapsed_time()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_elapsed_time(start:float, end:float) -> str:

    """

    Calculates elapsed time with an offset.

    Parameters:
    start (float) : Start time.
    end (float) : End time.

    Returns:
    print_value (string): The elapsed time in a human-readable format.

    """

    elapsed_time = end - start
    print_value = ""

    if(elapsed_time < 60.0):
        print_value = str(round(elapsed_time, 2)) + " seconds"
    elif(elapsed_time < 3600.0):
        print_value = str(round(elapsed_time / 60, 2)) + " minutes"
    else:
        print_value = str(round(elapsed_time / 3600, 2)) + " hours"

    return print_value

##-------------------start-of-Name---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Name(typing.NamedTuple):

    """
    
    Represents a Japanese name along with its equivalent english name.
    The Name class extends the NamedTuple class, allowing for the creation of a tuple with named fields.

    """

    jap : str
    eng : str

##-------------------start-of-ReplacementType---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class ReplacementType(enum.Flag):

    """

    Represents how a name should be replaced when dealing with honorifics and overall replacements.

    The ReplacementType class extends the Flag class, allowing for the combination of name markers using bitwise operations.
    
    Name Markers:
    - NONE : No specific name marker.
    - FULL_NAME : Represents a full name, first and last name.
    - FIRST_NAME : Represents the first name only.
    - FULL_AND_FIRST : Represents both the full name and the first name separately.
    - LAST_NAME : Represents the last name only.
    - FULL_AND_LAST : Represents both the full name and the last name.
    - FIRST_AND_LAST : Represents both the first name and the last name.
    - ALL_NAMES : Represents all possible names.

    """

    NONE = 0 
    FULL_NAME = 1 
    FIRST_NAME = 2 
    FULL_AND_FIRST = 3 
    LAST_NAME = 4 
    FULL_AND_LAST = 5 
    FIRST_AND_LAST = 6 
    ALL_NAMES = 7

##-------------------start-of-PathHandler---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class PathHandler():

    """
    
    Holds the paths for the different files used in the project.

    """

    script_dir = os.path.dirname(__file__)

    lib_dir = os.path.join(script_dir, "lib")
    examples_dir = os.path.join(os.path.dirname(os.path.dirname(script_dir)), "examples")
    
    katakana_words_path = os.path.join(lib_dir, "katakana_words.txt")

##-------------------start-of-demo_json---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

demo_json={
  "honorifics": {
    "ちゃん": "chan",
    "殿": "dono",
    "くん": "kun",
    "君": "kun",
    "後輩": "kōhai",
    "様": "sama",
    "さん": "san",
    "せんぱい": "senpai",
    "先輩": "senpai",
    "先生": "sensei",
    "氏": "shi",
    "上": "ue"
  },

  "single_words": {
    "β": "Beta",
    "後輩":"kōhai",
    "先輩":"senpai"

  },

  "unicode": {
    "\u2026":"...",
    "\u3000": " "
  },

  "phrases": {
    "高度育成高等学校": "Advanced Nurturing High School",
    "高育" : "ANHS",
    "ケヤキモール" : "Keyaki Mall",
    "プロテクトポイント": "Protection Point",
    "東京都高度育成高等学校":"Tokyo Metropolitan Advanced Nurturing High School"
  },

  "kutouten": {
    "「": "\"",
    "」": "\"",
    "『": "'",
    "』": "'",
    "、": ",",
    "─": "-",
    "～":"~",
    "！":"!",
    "？":"?",
    "％":"%",
    "（":"(",
    "）":")",
    "……。":"...",
    "…。":"...",
    "。": ".",
    "・":".",
    "…………":"...",
    "……": "...",
    "･･･":"...",
    "......":"...",
    ".....":"...",
    "....":"...",
    "---.":"---"
  },

  "name_like": {
    
  },

  "single_names": {
    "Akiyama": ["秋山"],
    "Anzai": ["安在"],
    "Ijūin": ["伊集院"],
    "Ishida": ["石田"],
    "Isoyama": ["磯山"],
    "Keisei": ["啓誠"],
    "Kijima": ["鬼島"],
    "Kisarazu": ["木更津"],
    "Kinugasa" :["衣笠"],
    "Mii": ["みー"],
    "Mika": ["美香"],
    "Ohba": ["大場"],
    "Sawada": ["沢田"],
    "Shiro": ["志朗"],
    "Sonezaki": ["曽根崎"],
    "Sōya": ["宗谷"],
    "Tomose":["トモセ"],
    "Yano": ["矢野"],
    "king": ["Wan-sama"]
    },


  "full_names": {
    "Amasawa Ichika": ["天沢","一夏"],
    "Amikura Mako": ["網倉","麻子"],
    "Andō Sayo" : ["安藤","紗代"],
    "Asahina Nazuna": ["朝比奈","なずな"],
    "Asama Hisashi": ["浅間","久"],
    "Ayanokōji Atsuomi": ["綾小路","篤臣"],
    "Ayanokōji Kiyotaka": ["綾小路","清隆"],
    "Azuma Sana": ["東","咲菜"],
    "Chabashira Sae": ["茶柱","佐枝"],
    "Enoshima Midoriko":["榎嶋","翠子"],
    "Hamaguchi Tetsuya": ["浜口","哲也"],
    "Hasebe Haruka": ["長谷部","波瑠加"],
    "Hashimoto Masayoshi": ["橋本","正義"],
    "Himeno Yuki":["姫野","ユキ"],
    "Hirata Yōsuke": ["平田","洋介"],
    "Hondō Ryōtarō": ["本堂","遼太郎"],
    "Horikita Manabu": ["堀北","学"],
    "Horikita Suzune": ["堀北","鈴音"],
    "Hoshinomiya Chie": ["星之宮","知恵"],
    "Hōsen Kazuomi": ["宝泉","和臣"],
    "Ibuki Mio": ["伊吹","澪"],
    "Ichinose Honami": ["一之瀬","帆波"],
    "Ike Kanji": ["池","寛治"],
    "Inogashira Kokoro": ["井の頭","心"],
    "Ishigami Kyō" : ["石上" , "京"],
    "Ishizaki Daichi": ["石崎","大地"],
    "Isomaru Yōkō": ["磯丸","容幸"],
    "Kamogawa Toshizō": ["鴨川","俊三"],
    "Kamuro Masumi": ["神室","真澄"],
    "Kaneda Satoru": ["金田","悟"],
    "Kanzaki Ryūji": ["神崎","隆二"],
    "Karuizawa Kei": ["軽井沢","恵"],
    "Katsuragi Kōhei": ["葛城","康平"],
    "Kikyō Kushida": ["桔梗","櫛田"],
    "Kinoshita Minori" : ["木下","美野里"],
    "Kiriyama Ikuto": ["桐山","生叶"],
    "Kiryūin Fūka": ["鬼龍院","楓花"],
    "Kitō Hayato": ["鬼頭","隼"],
    "Kobashi Yume": ["小橋","夢"],
    "Komiya Kyōgo": ["小宮","叶吾"],
    "Kondō Reo": ["近藤","玲音"],
    "Kōenji Rokusuke": ["高円寺","六助"],
    "Kōji Machida": ["浩二","町田"],
    "Kusuda Yukitsu": ["楠田","ゆきつ"],
    "Manabe Shiho": ["真鍋","志保"],
    "Mashima Tomonari": ["真嶋","智也"],
    "Matsushita Chiaki": ["松下","千秋"],
    "Miyake Akito": ["三宅","明人"],
    "Miyamoto Sōshi":["宮本","蒼士"],
    "Mori Nene": ["森","寧々"],
    "Morishita Ai": ["森下","藍"],
    "Morofuji Rika" : ["諸藤","リカ"],
    "Nagumo Miyabi": ["南雲","雅"],
    "Nanase Tsubasa": ["七瀬","翼"],
    "Naoe Jinnosuke": ["直江","仁之助"],
    "Nishino Takeko" : ["西野","武子"],
    "Okitani Kyōsuke": ["沖谷","京介"],
    "Onodera Kayano": ["小野寺","かや乃"],
    "Ryūen Kakeru": ["龍園","翔"],
    "Sakagami Kazuma": ["坂上","数馬"],
    "Sakayanagi Arisu": ["坂柳","有栖"],
    "Sakayanagi Narimori": ["坂柳","成守"],
    "Sakura Airi": ["佐倉","愛里"],
    "Satō Maya": ["佐藤","麻耶"],
    "Sanada Kousei": ["真田","康生"],
    "Shiba Katsunori": ["司馬","克典"],
    "Shibata Sō" : ["柴田","颯"],
    "Shiina Hiyori": ["椎名","ひより"],
    "Shinohara Satsuki": ["篠原","さつき"], 
    "Shiranami Chihiro": ["白波","千尋"],
    "Sotomura Hideo": ["外村","秀雄"],
    "Suchi Moeka": ["須知","萌香"],
    "Sudō Ken": ["須藤","健"],
    "Suzukake Tanji": ["鈴懸","鍛治"],
    "Tachibana Akane": ["橘","茜"],
    "Tachibana Kento": ["立花","賢人"],
    "Tokitō Hiroya": ["時任","裕也"],
    "Totsuka Yahiko": ["戸塚","弥彦"],
    "Tsubaki Sakurako": ["椿","桜子"],
    "Tsukishiro Tokinari": ["月城","常成"],
    "Utomiya Riku": ["宇都宮","陸"],
    "Wan Mei-Yui": ["王","美雨"],
    "Yabu Nanami" : ["藪","菜々美"],
    "Yagami Takuya": ["八神","拓也"],
    "Yamada Albert": ["山田","アルベルト"],
    "Yamamura Miki": ["山村","美紀"],
    "Yamanaka Ikuko": ["山中","郁子"],
    "Yamashita Saki" : ["鈴代","紗弓"],
    "Yamauchi Haruki": ["山内","春樹"],
    "Yukimura Teruhiko": ["幸村","輝彦"]
  },

  "enhanced_check_whitelist": {
    "Hoshinomiya Chie": ["星之宮","知恵"]
  }
  
}

##-------------------start-of-demo_txt---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

demo_txt="""
通学路には人だかりが出来ていた。冬休み中には見られなかった光景だ。
閑静な時の景色も嫌いじゃないが、意外と生徒の波を見る方が好きなのかも知れない。
あるいは、広がる視界に慣れてしまったのか。
終わりが近づく時を予感し、無意識のうちに惜しみ始めているのか。
「どうしたの清隆。立ち止まって」
温かみに包まれる右腕から、こちらを見上げる恋人の恵の顔が見えた。
潤った唇が目に留まる。出がけにお気に入りのリップをつけたのだろう。
「いや、何でもない」
そう呟いて２人で歩き出す。彼女と過ごす日常は、少なくとも退屈からは解放される。
黙っていてもお喋りが好きな恵が、その日その日にあった話題を自動的に提供してくれるからだ。ただし圧倒的に独りで過ごす時間とは無縁になっていく。
その２人で過ごす日々が必要なのか不必要なのかを問われると、半々だと答える。
必要な理由としては、対人による会話を繰り返すことで、少なからずオレにコミュニケーション能力を与えてくれていること。これは未熟なスキルを磨く貴重な機会だ。
一方で未熟だからこそ、相手に対して返答を失敗することも多い。
特に不機嫌な時の恵に対しては不正解を選んでしまうことも多く、その結果更に不機嫌にしてしまうケースは今でも絶えない。これは苦労する部分だ。
一方、個のスキルを磨く時間が削られることはデメリットだ。コミュニケーションと恋愛、そして異性を解剖していくメリットを除けば、その他多くを犠牲にしている。
「何、あたしの顔ジロジロみて」
「嫌だったか？」
「嫌じゃない、けど。......ん、またキスしたくなっちゃうじゃん。たくさん」
冬休みが終わる前日、恵とは朝から晩まで、部屋の中でゆっくりと過ごしたからな。
親しき若い男女が同じ空間にいれば、その行く末は多くを語るまでもないだろう。
自分の方へ右腕を抱き寄せるように恵はより力を込めてきた。
結局、学校の玄関に到着して靴から上履きに履き替える時を除き、終始教室まで２人はくっついたままだった。既に半数近くの生徒は登校したようで、クラスは賑わっている。
「皆、おっはよ～」
３学期の幕開け。クラスの友達に向かって恵がそう手を振った。絡めていた自身の腕をゆっくりと離して、またねとオレにウインクをする。そんな厚い愛情を残して去って行った後、教室の中ほどにある自分の席に移動して中身の少ない鞄を置く。
タブレット端末が授業に導入されてから必要なものは減ったが、それでも鞄は欠かせない。
「かーっ、見ててこっちが恥ずかしくなるような登校してくるなよ、綾小路」
既に教室に顔を出していた須藤が、気まずそうにそう声をかけてきた。
「腕組んで登校とか陽キャの極みってヤツだろ。くっそ、羨ましいぜ」
当人としては恥ずかしい光景だが、それ自体を羨ましいとは思っているらしい。
「言っておくがオレが希望したわけじゃない」
「いやそうだろうけどよ。つかおまえがアレを希望してたら超引くわ、絶対引く」
ないわー、と繰り返し呟きながらも顔を近づけてくる。
「イチャイチャするのも結構だけどな、冬休み中に１年が補導されたって学校のメール見たか？ おまえなら心配ないだろうけど、一応気をつけろよ？」
「そう言えばそんなメールもあったな」
冬休みの終盤、学校から１年生の２名に罰則が科されるメールが届いた。
匿名となっていため名前は分からないが、男女２名が屋外で不純異性交遊に値する行為を取っていたところを第三者に目撃されたというもの。
性的刺激を目的とした行為は原則禁止されているため、当然罰則の対象になる。
「部屋の中だけにしときゃいいのによ。そこんところ先輩のおまえはどうなんだよ」
「どうなんだよって、何が」
「......外で色々してえとか思うもん......なのか、とかさ」
恥ずかしがるなら聞かなければいいのにと思いつつ、突っ込むのはやめておく。
「メールの通りとしか言えないな。学校の敷地内は人目と監視カメラで溢れてる。変な行為をすれば見つかるリスクが高い。だから本能に身を任せるような選択はしない」
「お、おう。なんか、綾小路にしか出来そうにない意見だな......ちょっと引くわ」
全然関係ない形で結局須藤には引かれてしまったようだ。
「───ふうっ」
特に意識をしたわけではない、須藤のやや重ためのため息が聞こえた。無意識のため息のようだったが、自ら発した後で気が付いたようで慌てて謝罪してきた。
「今のはおまえのことでじゃないからな。悪い、そう受け取られるため息だったかも」
「気にしてない。でもどうかしたのか？」
人前で大声を挙げる機会はこれまで何度もあったが、ため息が多い生徒じゃなかった。
その変化はけして軽視できるものではない。
「最近ちょっと疲れが溜まっててよ。勉強とスポーツの両立が出来てると思ってたのにキツイと感じることが増えてきた。って......なんてな」
ため息の理由を話したことが失敗だったと思ったのか、須藤はそう誤魔化した。
これ以上心配をする言葉をかけるとかえって逆効果になりそうだな。
なので、一言だけアドバイスを伝えておく。
「知識を詰め込むにしても急げばその分零れ落ちやすい。急がば回れだ」
「......だな。つか、今日からまたよろしくな」
頭を切り替え、そう笑って言ってから自分の席へと向かった。
直後、新たに教室へとやってきた佐藤がクラスメイトに挨拶しつつオレの傍を通る。
「朝から熱々だったね、２人とも」
そう小声で呟き、ご馳走様、と付け加えてから女子グループに合流する。
どうやら恵との登校を後ろの方から目撃していたようだ。

１

冬休みが明けても、学生も教師も基本的にやることは何も変わらない。
茶柱先生がクラスにやってくると、新年の挨拶を軽く済ませ教壇に手をついた。
「今日から３学期が始まる。１月は行く、２月は逃げる、３月は去ると言われるようにこの時期はあっという間に駆け抜けていくものだ。日々を惰性で過ごすことのないよう、気を引き締めて過ごすように」
誰も指摘しないが、ちょっと面白いのは茶柱先生の後ろ髪。若干だが寝癖のようなものがついている。今朝は起床時刻が遅く慌てていたのだろうか。
生徒たちを引き締める言葉を告げたものの、やや説得力に欠けることとなった。
朝のホームルーム終了を告げ、教室を後にしようとした茶柱先生だったが、出入口の近くで足を止めた。
「１つ通達事項を忘れていた。来月にはこの学校で初めての『二者面談』を行う予定だ。これまでの学校生活の話も織り交ぜつつ進路、就職に関する話を中心にしていくことになるだろう。当然ながら、既におまえたちの保護者へ聞き取り調査も終えている」
振り返りながらクラスメイトたちにそう声をかけた。
進路を生徒個人だけで決める家庭もあるだろうが、多くは親の意見も参考にする。
学校側は生徒のいないところでもちゃんと動いている証拠だ。
「この学校にもそんなのあったんスね。てっきり無いものだと思ってました」
とにもかくにも誰よりも先に口が出る池の発言だ。誰も驚かない。
「高校が義務教育ではないと言っても、保護者の言葉を完全に無視して進路を決定させるわけにも行かないからな。当然、いずれ時期が来れば三者面談も実施される」
三者面談。あの男が再び出張って来る可能性もあるということだろうか。
いや、もうこの学校で会うことはないと吐き捨てていたが、果たしてどうなるのか。
その問題は気になりつつも、まずは２月の二者面談だ。と言ってもオレの場合は将来も何も、自由意思でどうにもならないと判断しているので関係ないと言えば関係ない。
そういう意味では、茶柱先生が片足程度でもこちらの事情を知っているのは非常にありがたい。深い話し合いなど必要ないため、形式だけのものになるだろう。
反面クラスメイトたちにとって二者、三者面談は大きな岐路になることは間違いない。
真っすぐ己の進路を見据え突き進むのか、迂回して他の道を探すのか。
自分だけでは見えてこない部分に、親と教師が手掛かりを与えてくれるはず。
「気になることがあれば、私に直接聞きに来るといい」
これで伝えるべきことを伝え終えたと、茶柱先生は扉に手をかけた。
そして後ろ手で閉じた扉が閉まっていく瞬間もう片方の手で後頭部を触る仕草を見せる。
どうやら寝癖には自分でも気が付いていたらしい。

２

茶柱先生が教室を出た後、クラスは一気に二者面談、そして将来のことについての話題でもちきりになった。
「そろそろどうするか考えておかないとだよね」
「Ａクラスで卒業できるパターンと、そうじゃないパターンをまずは考えないといけないわけでしょ？ ねえ平田くんはどうするつもりなの？」
クラスの中心に鎮座する洋介の周りに集まった女子たちがそう話題を振る。
「僕はＡクラスの特権関係なく大学進学を視野に入れているよ。両親もそれを望んでいるのは早いうちから聞いているからね」
聞き耳を立てるつもりはないが、聞こえてくるのだから不可抗力。
洋介は現段階で就職の意思は芽生えていないようで進学前提の考えを持っている。
勉強に取り組む姿勢や実際の学力を考慮すれば、自然な流れ。
Ａクラスの特権があろうとなかろうと、取り組む力を持っていなければ権利を活かしきれないからな。
ただ、これは全てのことに言える話だ。
「そうなんだ。私はてっきりサッカー選手にでもなるのかと思ってたー」
「はは、それはちょっと。仮にＡクラスの特権を使って無理やりプロになっても、実力が見合ってなければすぐに解雇されるのは目に見えてるからね。大学に行ってもサッカーは続けるつもりだけど、あくまでも趣味かな」
スポーツ関連への就職は、やはりその後のハードルが極めて高いと言える。
権利を行使してでも行くべき者がいるとすれば、実力があっても何らかの理由で発掘されておらず埋もれている場合や別に問題を抱えて正規ルートを辿れない場合などだ。
ではこのＡクラス卒業の恩恵を上手く活用するにはどうするのが正しいのか。
クラス内でも秀才としての立場を確立している啓誠が口を開いた。
「Ａクラスの特権って話なら、断然大手企業に就職するべきだ。露骨に能力が追い付いていない場合は例外としても、人並みに働けるなら滅多なことじゃ解雇されない。入った者勝ちの世界に飛び込ませてもらうのが一番賢い使い方じゃないのか」
そんな啓誠の理に適った発言に、感心したようにクラスメイトたちが頷く。
会社は人を雇う以上、大きな責任が生まれる。
大きな失態をしない限り、単に気に入らないといった理由で解雇することは不当だ。
新設されたばかりの学校でもない高育の存在は政府公認ということもあって広く知られていることだろう。これまでに何人もＡクラスで卒業した生徒は受け入れられている。
そういう意味でも大手企業を選べば安心して、長く職務を全うすることが出来る。
「効率だけを考えると幸村くんの選択は正しいかも知れないね。でも、僕はなりたい職業を目指すことも大切にした方がいいんじゃないかなとは思うかな」
それもまた正しい答えの１つだ。１度きりの人生、お金や安定した職のためだけに人生を送ることを、まだ決断しなくてもいい。
理想を追う就職先か現実を追う就職先か。
この場にいる生徒たちは遅かれ早かれ、その分岐点に立つことになる。
正直、どんな選択にも正解はあるし不正解はあるのだろう。
オレの卒業後に待つ未来は今のところ１つだけだが、それも正解だったのか不正解だったのかを知るのは遥か先のこと。
正しい人生だったと思えるのか否か。
生涯を振り返る時、どう結論付けているのかで本当の答えが出る。

３

さて冬休み明け一発目の昼食時間がやってきた。既に恵は、佐藤たち女子グループを結成して食堂に向かうようだ。恋人ばかりに目を向けず友人を大切に。とても重要なことだ。廊下に出てそんな恵の後ろ姿をそれとなく見守ってみると、綺麗に横一列だった。
「女子はなんでいつも、４人も５人も関係なく横並びになるんだろうな」
「そんなこと私に聞かれても困るわ。横並びはただの迷惑行為よ」
背後に立つ堀北に質問を投げかけてみたが、その理由は知らないらしい。
「それより、あなた背中に目でも付いてるの？ どうやって気付いたのか不思議だわ」
「不思議は不思議のままにしておいた方がいいんじゃないか？」
「教える気はないってことね」
「なら、女子がどうして横並びになるのかの理由を教えてくれたら考えてやってもいい」
「それは堀北さんには答えられない質問で酷だよ。列を作るほど友達いないんだし」
堀北に続いて櫛田が姿を見せる。
「カーストがあるからね。廊下を塞いで邪魔になったとしても、グループを健全に維持していくためには必要なこともあるんだよ」
「なるほど。前を歩く人間に従うような形を自然と避けてるわけか」
「多分ね。皆口にしてるわけじゃないけど、何となく察してのことなんだと思う」
だとすれば女性に多い集団心理からくるメカニズムとも言えるかも知れないな。
「実に下らない理由ね。周りのことを考えて歩くべきだわ」
「はいはい、友達のいない人はそう言えていいよね」
「あなた私に喧嘩を売っているの？」
「売ってないとでも思ってたの？ 笑えるぅ」
"""