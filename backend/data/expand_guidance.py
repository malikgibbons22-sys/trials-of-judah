"""Expand Guidance categories with additional verses."""
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "verses.json"

def add_verses(data, slug, new_verses):
    for cat in data['categories']:
        if cat['slug'] == slug:
            existing_refs = {v['reference'] for v in cat['verses']}
            for v in new_verses:
                if v['reference'] not in existing_refs:
                    cat['verses'].append(v)
            return

def v(book, ch, vs, ve, ref, note, date, kjv, esv):
    return {"book":book,"chapter":ch,"verse_start":vs,"verse_end":ve,
            "reference":ref,"context_note":note,"date_written":date,"kjv":kjv,"esv":esv}

def main():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # ── CHOOSING A SPOUSE ──
    add_verses(data, 'choosing-a-spouse', [
        v("Ruth",1,16,17,"Ruth 1:16-17","Ruth's declaration of loyalty to Naomi, her mother-in-law","c. 1100 BC",
          "And Ruth said, Intreat me not to leave thee, or to return from following after thee: for whither thou goest, I will go; and where thou lodgest, I will lodge: thy people shall be my people, and thy God my God: Where thou diest, will I die, and there will I be buried: the LORD do so to me, and more also, if ought but death part thee and me.",
          'But Ruth said, "Do not urge me to leave you or to return from following you. For where you go I will go, and where you lodge I will lodge. Your people shall be my people, and your God my God. Where you die I will die, and there will I be buried. May the LORD do so to me and more also if anything but death parts me from you."'),
        v("Ecclesiastes",4,9,12,"Ecclesiastes 4:9-12","Solomon on the strength of companionship","c. 935 BC",
          "Two are better than one; because they have a good reward for their labour. For if they fall, the one will lift up his fellow: but woe to him that is alone when he falleth; for he hath not another to help him up. Again, if two lie together, then they have heat: but how can one be warm alone? And if one prevail against him, two shall withstand him; and a threefold cord is not quickly broken.",
          "Two are better than one, because they have a good reward for their toil. For if they fall, one will lift up his fellow. But woe to him who is alone when he falls and has not another to lift him up! Again, if two lie together, they keep warm, but how can one keep warm alone? And though a man might prevail against one who is alone, two will withstand him--a threefold cord is not quickly broken."),
        v("1 Peter",3,7,None,"1 Peter 3:7","Peter instructing husbands on honoring their wives","c. 64-65 AD",
          "Likewise, ye husbands, dwell with them according to knowledge, giving honour unto the wife, as unto the weaker vessel, and as being heirs together of the grace of life; that your prayers be not hindered.",
          "Likewise, husbands, live with your wives in an understanding way, showing honor to the woman as the weaker vessel, since they are heirs with you of the grace of life, so that your prayers may not be hindered."),
        v("Hebrews",13,4,None,"Hebrews 13:4","The author of Hebrews on the honor of marriage","c. 64-68 AD",
          "Marriage is honourable in all, and the bed undefiled: but whoremongers and adulterers God will judge.",
          "Let marriage be held in honor among all, and let the marriage bed be undefiled, for God will judge the sexually immoral and adulterous."),
        v("Amos",3,3,None,"Amos 3:3","Amos the prophet on the necessity of agreement","c. 760-750 BC",
          "Can two walk together, except they be agreed?",
          "Do two walk together, unless they have agreed to meet?"),
        v("Colossians",3,18,19,"Colossians 3:18-19","Paul instructing husbands and wives at Colossae","c. 60-62 AD",
          "Wives, submit yourselves unto your own husbands, as it is fit in the Lord. Husbands, love your wives, and be not bitter against them.",
          "Wives, submit to your husbands, as is fitting in the Lord. Husbands, love your wives, and do not be harsh with them."),
    ])

    # ── BUYING A HOME ──
    add_verses(data, 'buying-a-home', [
        v("Proverbs",12,7,None,"Proverbs 12:7","Solomon contrasting the wicked and the righteous household","c. 970-700 BC",
          "The wicked are overthrown, and are not: but the house of the righteous shall stand.",
          "The wicked are overthrown and are no more, but the house of the righteous will stand."),
        v("Isaiah",32,18,None,"Isaiah 32:18","Isaiah prophesying a time of peace and secure dwellings","c. 740-680 BC",
          "And my people shall dwell in a peaceable habitation, and in sure dwellings, and in quiet resting places;",
          "My people will abide in a peaceful habitation, in secure dwellings, and in quiet resting places."),
        v("Deuteronomy",28,6,None,"Deuteronomy 28:6","Moses declaring blessings for obedience","c. 1406 BC",
          "Blessed shalt thou be when thou comest in, and blessed shalt thou be when thou goest out.",
          "Blessed shall you be when you come in, and blessed shall you be when you go out."),
        v("Proverbs",14,1,None,"Proverbs 14:1","Solomon on the wise woman who builds her house","c. 970-700 BC",
          "Every wise woman buildeth her house: but the foolish plucketh it down with her hands.",
          "The wisest of women builds her house, but folly with her own hands tears it down."),
        v("Matthew",7,24,25,"Matthew 7:24-25","Jesus teaching about building on a firm foundation","c. 50-70 AD",
          "Therefore whosoever heareth these sayings of mine, and doeth them, I will liken him unto a wise man, which built his house upon a rock: And the rain descended, and the floods came, and the winds blew, and beat upon that house; and it fell not: for it was founded upon a rock.",
          'Everyone then who hears these words of mine and does them will be like a wise man who built his house on the rock. And the rain fell, and the floods came, and the winds blew and beat on that house, but it did not fall, because it had been founded on the rock.'),
    ])

    # ── CAREER PATH ──
    add_verses(data, 'career-path', [
        v("Psalms",90,17,None,"Psalms 90:17","Moses praying for God's favor on the work of Israel's hands","c. 1400 BC",
          "And let the beauty of the LORD our God be upon us: and establish thou the work of our hands upon us; yea, the work of our hands establish thou it.",
          "Let the favor of the Lord our God be upon us, and establish the work of our hands upon us; yes, establish the work of our hands!"),
        v("Proverbs",12,11,None,"Proverbs 12:11","Solomon on the value of honest labor","c. 970-700 BC",
          "He that tilleth his land shall be satisfied with bread: but he that followeth vain persons is void of understanding.",
          "Whoever works his land will have plenty of bread, but he who follows worthless pursuits lacks sense."),
        v("Proverbs",22,29,None,"Proverbs 22:29","Solomon on the reward of skillful work","c. 970-700 BC",
          "Seest thou a man diligent in his business? he shall stand before kings; he shall not stand before mean men.",
          "Do you see a man skillful in his work? He will stand before kings; he will not stand before obscure men."),
        v("Isaiah",64,8,None,"Isaiah 64:8","Isaiah acknowledging God as the potter who shapes his people","c. 740-680 BC",
          "But now, O LORD, thou art our father; we are the clay, and thou our potter; and we all are the work of thy hand.",
          "But now, O LORD, you are our Father; we are the clay, and you are our potter; we are all the work of your hand."),
        v("1 Corinthians",10,31,None,"1 Corinthians 10:31","Paul instructing the believers in Corinth to glorify God in all things","c. 55 AD",
          "Whether therefore ye eat, or drink, or whatsoever ye do, do all to the glory of God.",
          "So, whether you eat or drink, or whatever you do, do all to the glory of God."),
    ])

    # ── FINANCIAL DECISIONS ──
    add_verses(data, 'financial-decisions', [
        v("Proverbs",3,9,10,"Proverbs 3:9-10","Solomon on honoring the Lord with one's wealth","c. 970-700 BC",
          "Honour the LORD with thy substance, and with the firstfruits of all thine increase: So shall thy barns be filled with plenty, and thy presses shall burst out with new wine.",
          "Honor the LORD with your wealth and with the firstfruits of all your produce; then your barns will be filled with plenty, and your vats will be bursting with wine."),
        v("Deuteronomy",8,18,None,"Deuteronomy 8:18","Moses reminding Israel that God gives the power to gain wealth","c. 1406 BC",
          "But thou shalt remember the LORD thy God: for it is he that giveth thee power to get wealth, that he may establish his covenant which he sware unto thy fathers, as it is this day.",
          "You shall remember the LORD your God, for it is he who gives you power to get wealth, that he may confirm his covenant that he swore to your fathers, as it is this day."),
        v("Philippians",4,19,None,"Philippians 4:19","Paul assuring the believers at Philippi of God's provision","c. 61-62 AD",
          "But my God shall supply all your need according to his riches in glory by Christ Jesus.",
          "And my God will supply every need of yours according to his riches in glory in Christ Jesus."),
        v("Hebrews",13,5,None,"Hebrews 13:5","The author of Hebrews on contentment and God's presence","c. 64-68 AD",
          "Let your conversation be without covetousness; and be content with such things as ye have: for he hath said, I will never leave thee, nor forsake thee.",
          'Keep your life free from love of money, and be content with what you have, for he has said, "I will never leave you nor forsake you."'),
        v("Proverbs",28,20,None,"Proverbs 28:20","Solomon on faithfulness versus haste in gaining wealth","c. 970-700 BC",
          "A faithful man shall abound with blessings: but he that maketh haste to be rich shall not be innocent.",
          "A faithful man will abound with blessings, but whoever hastens to be rich will not go unpunished."),
        v("Romans",13,8,None,"Romans 13:8","Paul writing to the believers in Rome about owing nothing but love","c. 57 AD",
          "Owe no man any thing, but to love one another: for he that loveth another hath fulfilled the law.",
          "Owe no one anything, except to love each other, for the one who loves another has fulfilled the law."),
    ])

    # ── RAISING CHILDREN ──
    add_verses(data, 'raising-children', [
        v("Psalms",127,3,5,"Psalms 127:3-5","A psalm of Solomon on children as a heritage from the Lord","c. 970 BC",
          "Lo, children are an heritage of the LORD: and the fruit of the womb is his reward. As arrows are in the hand of a mighty man; so are children of the youth. Happy is the man that hath his quiver full of them: they shall not be ashamed, but they shall speak with the enemies in the gate.",
          "Behold, children are a heritage from the LORD, the fruit of the womb a reward. Like arrows in the hand of a warrior are the children of one's youth. Blessed is the man who fills his quiver with them! He shall not be put to shame when he speaks with his enemies in the gate."),
        v("Proverbs",13,24,None,"Proverbs 13:24","Solomon on the necessity of discipline in love","c. 970-700 BC",
          "He that spareth his rod hateth his son: but he that loveth him chasteneth him betimes.",
          "Whoever spares the rod hates his son, but he who loves him is diligent to discipline him."),
        v("Isaiah",54,13,None,"Isaiah 54:13","Isaiah prophesying that the children of Israel will be taught by the Lord","c. 740-680 BC",
          "And all thy children shall be taught of the LORD; and great shall be the peace of thy children.",
          "All your children shall be taught by the LORD, and great shall be the peace of your children."),
        v("Mark",10,14,None,"Mark 10:14","Jesus rebuking those who turned children away","c. 55-70 AD",
          "But when Jesus saw it, he was much displeased, and said unto them, Suffer the little children to come unto me, and forbid them not: for of such is the kingdom of God.",
          'But when Jesus saw it, he was indignant and said to them, "Let the children come to me; do not hinder them, for to such belongs the kingdom of God."'),
        v("Deuteronomy",11,19,None,"Deuteronomy 11:19","Moses commanding Israel to teach their children diligently","c. 1406 BC",
          "And ye shall teach them your children, speaking of them when thou sittest in thine house, and when thou walkest by the way, when thou liest down, and when thou risest up.",
          "You shall teach them to your children, talking of them when you are sitting in your house, and when you are walking by the way, and when you lie down, and when you rise."),
    ])

    # ── FORGIVENESS & RECONCILIATION ──
    add_verses(data, 'forgiveness-reconciliation', [
        v("Genesis",50,20,None,"Genesis 50:20","Joseph speaking to his brothers who had sold him into slavery","c. 1446-1406 BC",
          "But as for you, ye thought evil against me; but God meant it unto good, to bring to pass, as it is this day, to save much people alive.",
          "As for you, you meant evil against me, but God meant it for good, to bring it about that many people should be kept alive, as they are today."),
        v("Luke",15,20,24,"Luke 15:20-24","Jesus telling the parable of the prodigal son","c. 60-62 AD",
          "And he arose, and came to his father. But when he was yet a great way off, his father saw him, and had compassion, and ran, and fell on his neck, and kissed him. And the son said unto him, Father, I have sinned against heaven, and in thy sight, and am no more worthy to be called thy son. But the father said to his servants, Bring forth the best robe, and put it on him; and put a ring on his hand, and shoes on his feet: And bring hither the fatted calf, and kill it; and let us eat, and be merry: For this my son was dead, and is alive again; he was lost, and is found. And they began to be merry.",
          'And he arose and came to his father. But while he was still a long way off, his father saw him and felt compassion, and ran and embraced him and kissed him. And the son said to him, "Father, I have sinned against heaven and before you. I am no longer worthy to be called your son." But the father said to his servants, "Bring quickly the best robe, and put it on him, and put a ring on his hand, and shoes on his feet. And bring the fattened calf and kill it, and let us eat and celebrate. For this my son was dead, and is alive again; he was lost, and is found." And they began to celebrate.'),
        v("Colossians",3,12,14,"Colossians 3:12-14","Paul urging the believers at Colossae to clothe themselves in compassion","c. 60-62 AD",
          "Put on therefore, as the elect of God, holy and beloved, bowels of mercies, kindness, humbleness of mind, meekness, longsuffering; Forbearing one another, and forgiving one another, if any man have a quarrel against any: even as Christ forgave you, so also do ye. And above all these things put on charity, which is the bond of perfectness.",
          "Put on then, as God's chosen ones, holy and beloved, compassionate hearts, kindness, humility, meekness, and patience, bearing with one another and, if one has a complaint against another, forgiving each other; as the Lord has forgiven you, so you also must forgive. And above all these put on love, which binds everything together in perfect harmony."),
        v("Psalms",103,12,None,"Psalms 103:12","David praising God for removing transgressions","c. 1000-400 BC",
          "As far as the east is from the west, so far hath he removed our transgressions from us.",
          "As far as the east is from the west, so far does he remove our transgressions from us."),
        v("Isaiah",1,18,None,"Isaiah 1:18","God inviting Israel to reason together about forgiveness","c. 740-680 BC",
          "Come now, and let us reason together, saith the LORD: though your sins be as scarlet, they shall be as white as snow; though they be red like crimson, they shall be as wool.",
          '"Come now, let us reason together, says the LORD: though your sins are like scarlet, they shall be as white as snow; though they are red like crimson, they shall become like wool."'),
    ])

    # ── MOVING & RELOCATION ──
    add_verses(data, 'moving-relocation', [
        v("Psalms",121,7,8,"Psalms 121:7-8","A psalm of ascent declaring God's protection in travel","c. 1000-400 BC",
          "The LORD shall preserve thee from all evil: he shall preserve thy soul. The LORD shall preserve thy going out and thy coming in from this time forth, and even for evermore.",
          "The LORD will keep you from all evil; he will keep your life. The LORD will keep your going out and your coming in from this time forth and forevermore."),
        v("Isaiah",30,21,None,"Isaiah 30:21","Isaiah on hearing God's direction behind you","c. 740-680 BC",
          "And thine ears shall hear a word behind thee, saying, This is the way, walk ye in it, when ye turn to the right hand, and when ye turn to the left.",
          'And your ears shall hear a word behind you, saying, "This is the way, walk in it," when you turn to the right or when you turn to the left.'),
        v("Deuteronomy",31,8,None,"Deuteronomy 31:8","Moses encouraging Joshua before entering the promised land","c. 1406 BC",
          "And the LORD, he it is that doth go before thee; he will be with thee, he will not fail thee, neither forsake thee: fear not, neither be dismayed.",
          "It is the LORD who goes before you. He will be with you; he will not leave you or forsake you. Do not fear or be dismayed."),
        v("Ruth",1,16,None,"Ruth 1:16","Ruth declaring her loyalty as she relocates with Naomi","c. 1100 BC",
          "And Ruth said, Intreat me not to leave thee, or to return from following after thee: for whither thou goest, I will go; and where thou lodgest, I will lodge: thy people shall be my people, and thy God my God:",
          'But Ruth said, "Do not urge me to leave you or to return from following you. For where you go I will go, and where you lodge I will lodge. Your people shall be my people, and your God my God."'),
        v("Psalms",139,7,10,"Psalms 139:7-10","David on God's presence wherever one goes","c. 1000-400 BC",
          "Whither shall I go from thy spirit? or whither shall I flee from thy presence? If I ascend up into heaven, thou art there: if I make my bed in hell, behold, thou art there. If I take the wings of the morning, and dwell in the uttermost parts of the sea; Even there shall thy hand lead me, and thy right hand shall hold me.",
          "Where shall I go from your Spirit? Or where shall I flee from your presence? If I ascend to heaven, you are there! If I make my bed in Sheol, you are there! If I take the wings of the morning and dwell in the uttermost parts of the sea, even there your hand shall lead me, and your right hand shall hold me."),
    ])

    # ── STARTING A BUSINESS ──
    add_verses(data, 'starting-a-business', [
        v("Psalms",37,4,None,"Psalms 37:4","David on delighting in the Lord to receive heart's desires","c. 1000-400 BC",
          "Delight thyself also in the LORD; and he shall give thee the desires of thine heart.",
          "Delight yourself in the LORD, and he will give you the desires of your heart."),
        v("Proverbs",3,5,6,"Proverbs 3:5-6","Solomon on trusting the Lord in all decisions","c. 970-700 BC",
          "Trust in the LORD with all thine heart; and lean not unto thine own understanding. In all thy ways acknowledge him, and he shall direct thy paths.",
          "Trust in the LORD with all your heart, and do not lean on your own understanding. In all your ways acknowledge him, and he will make straight your paths."),
        v("Joshua",1,8,None,"Joshua 1:8","God instructing Joshua to meditate on the law for success","c. 1400 BC",
          "This book of the law shall not depart out of thy mouth; but thou shalt meditate therein day and night, that thou mayest observe to do according to all that is written therein: for then thou shalt make thy way prosperous, and then thou shalt have good success.",
          "This Book of the Law shall not depart from your mouth, but you shall meditate on it day and night, so that you may be careful to do according to all that is written in it. For then you will make your way prosperous, and then you will have good success."),
        v("Proverbs",10,4,None,"Proverbs 10:4","Solomon on the reward of diligent hands","c. 970-700 BC",
          "He becometh poor that dealeth with a slack hand: but the hand of the diligent maketh rich.",
          "A slack hand causes poverty, but the hand of the diligent makes rich."),
        v("Ecclesiastes",11,6,None,"Ecclesiastes 11:6","Solomon on sowing broadly without knowing what will prosper","c. 935 BC",
          "In the morning sow thy seed, and in the evening withhold not thine hand: for thou knowest not whether shall prosper, either this or that, or whether they both shall be alike good.",
          "In the morning sow your seed, and at evening withhold not your hand, for you do not know which will prosper, this or that, or whether both alike will be good."),
        v("Proverbs",13,4,None,"Proverbs 13:4","Solomon on the desires of the diligent being fulfilled","c. 970-700 BC",
          "The soul of the sluggard desireth, and hath nothing: but the soul of the diligent shall be made fat.",
          "The soul of the sluggard craves and gets nothing, while the soul of the diligent is richly supplied."),
    ])

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    total = sum(len(c['verses']) for c in data['categories'])
    print(f"Total: {total} verses across {len(data['categories'])} categories")
    for c in data['categories']:
        print(f"  {c['slug']:30s} {len(c['verses'])} verses")

if __name__ == '__main__':
    main()
