"""Expand verses.json with additional verses per category."""
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

    # ── ANGER ──
    add_verses(data, 'anger', [
        v("Proverbs",15,18,None,"Proverbs 15:18","Solomon contrasts the wrathful and the patient","c. 970-700 BC",
          "A wrathful man stirreth up strife: but he that is slow to anger appeaseth strife.",
          "A hot-tempered man stirs up strife, but he who is slow to anger quiets contention."),
        v("Proverbs",16,32,None,"Proverbs 16:32","Solomon on the strength of self-control","c. 970-700 BC",
          "He that is slow to anger is better than the mighty; and he that ruleth his spirit than he that taketh a city.",
          "Whoever is slow to anger is better than the mighty, and he who rules his spirit than he who takes a city."),
        v("Matthew",5,22,None,"Matthew 5:22","Jesus teaching in the Sermon on the Mount","c. 50-70 AD",
          "But I say unto you, That whosoever is angry with his brother without a cause shall be in danger of the judgment: and whosoever shall say to his brother, Raca, shall be in danger of the council: but whosoever shall say, Thou fool, shall be in danger of hell fire.",
          "But I say to you that everyone who is angry with his brother will be liable to judgment; whoever insults his brother will be liable to the council; and whoever says, 'You fool!' will be liable to the hell of fire."),
        v("Romans",12,19,None,"Romans 12:19","Paul writing to the believers in Rome about leaving vengeance to God","c. 57 AD",
          "Dearly beloved, avenge not yourselves, but rather give place unto wrath: for it is written, Vengeance is mine; I will repay, saith the Lord.",
          'Beloved, never avenge yourselves, but leave it to the wrath of God, for it is written, "Vengeance is mine, I will repay, says the Lord."'),
        v("Proverbs",22,24,25,"Proverbs 22:24-25","Solomon warns against keeping company with the angry","c. 970-700 BC",
          "Make no friendship with an angry man; and with a furious man thou shalt not go: Lest thou learn his ways, and get a snare to thy soul.",
          "Make no friendship with a man given to anger, nor go with a wrathful man, lest you learn his ways and entangle yourself in a snare."),
        v("Ephesians",4,31,None,"Ephesians 4:31","Paul instructing the believers in Ephesus to put away bitterness","c. 60-62 AD",
          "Let all bitterness, and wrath, and anger, and clamour, and evil speaking, be put away from you, with all malice:",
          "Let all bitterness and wrath and anger and clamor and slander be put away from you, along with all malice."),
        v("Proverbs",19,11,None,"Proverbs 19:11","Solomon on the glory of overlooking an offense","c. 970-700 BC",
          "The discretion of a man deferreth his anger; and it is his glory to pass over a transgression.",
          "Good sense makes one slow to anger, and it is his glory to overlook an offense."),
    ])

    # ── LUST ──
    add_verses(data, 'lust', [
        v("Proverbs",6,25,None,"Proverbs 6:25","Solomon warns against the allure of the adulterous","c. 970-700 BC",
          "Lust not after her beauty in thine heart; neither let her take thee with her eyelids.",
          "Do not desire her beauty in your heart, and do not let her capture you with her eyelashes."),
        v("James",1,14,15,"James 1:14-15","James, brother of Jesus, on the progression of temptation","c. 45-49 AD",
          "But every man is tempted, when he is drawn away of his own lust, and enticed. Then when lust hath conceived, it bringeth forth sin: and sin, when it is finished, bringeth forth death.",
          "But each person is tempted when he is lured and enticed by his own desire. Then desire when it has conceived gives birth to sin, and sin when it is fully grown brings forth death."),
        v("Colossians",3,5,None,"Colossians 3:5","Paul urging the believers at Colossae to put to death earthly desires","c. 60-62 AD",
          "Mortify therefore your members which are upon the earth; fornication, uncleanness, inordinate affection, evil concupiscence, and covetousness, which is idolatry:",
          "Put to death therefore what is earthly in you: sexual immorality, impurity, passion, evil desire, and covetousness, which is idolatry."),
        v("Proverbs",4,23,None,"Proverbs 4:23","Solomon on guarding the heart as the source of life","c. 970-700 BC",
          "Keep thy heart with all diligence; for out of it are the issues of life.",
          "Keep your heart with all vigilance, for from it flow the springs of life."),
        v("1 Peter",2,11,None,"1 Peter 2:11","Peter writing to the scattered believers about abstaining from fleshly lusts","c. 64-65 AD",
          "Dearly beloved, I beseech you as strangers and pilgrims, abstain from fleshly lusts, which war against the soul;",
          "Beloved, I urge you as sojourners and exiles to abstain from the passions of the flesh, which wage war against your soul."),
        v("Psalms",119,9,11,"Psalms 119:9-11","The psalmist on keeping one's way pure through God's word","c. 1000-400 BC",
          "Wherewithal shall a young man cleanse his way? by taking heed thereto according to thy word. With my whole heart have I sought thee: O let me not wander from thy commandments. Thy word have I hid in mine heart, that I might not sin against thee.",
          "How can a young man keep his way pure? By guarding it according to your word. With my whole heart I seek you; let me not wander from your commandments! I have stored up your word in my heart, that I might not sin against you."),
    ])

    # ── FEAR ──
    add_verses(data, 'fear', [
        v("Psalms",34,4,None,"Psalms 34:4","David praising God for deliverance from all his fears","c. 1000-400 BC",
          "I sought the LORD, and he heard me, and delivered me from all my fears.",
          "I sought the LORD, and he answered me and delivered me from all my fears."),
        v("Isaiah",43,1,None,"Isaiah 43:1","God speaking through Isaiah to reassure Israel","c. 740-680 BC",
          "But now thus saith the LORD that created thee, O Jacob, and he that formed thee, O Israel, Fear not: for I have redeemed thee, I have called thee by thy name; thou art mine.",
          'But now thus says the LORD, he who created you, O Jacob, he who formed you, O Israel: "Fear not, for I have redeemed you; I have called you by name, you are mine."'),
        v("Psalms",91,1,2,"Psalms 91:1-2","A psalm of trust in God's protection","c. 1000-400 BC",
          "He that dwelleth in the secret place of the most High shall abide under the shadow of the Almighty. I will say of the LORD, He is my refuge and my fortress: my God; in him will I trust.",
          'He who dwells in the shelter of the Most High will abide in the shadow of the Almighty. I will say to the LORD, "My refuge and my fortress, my God, in whom I trust."'),
        v("Psalms",118,6,None,"Psalms 118:6","A psalm of thanksgiving for God's faithfulness","c. 1000-400 BC",
          "The LORD is on my side; I will not fear: what can man do unto me?",
          "The LORD is on my side; I will not fear. What can man do to me?"),
        v("Hebrews",13,6,None,"Hebrews 13:6","The author of Hebrews encouraging confidence in God","c. 64-68 AD",
          "So that we may boldly say, The Lord is my helper, and I will not fear what man shall do unto me.",
          'So we can confidently say, "The Lord is my helper; I will not fear; what can man do to me?"'),
        v("Matthew",10,28,None,"Matthew 10:28","Jesus instructing his disciples before sending them out","c. 50-70 AD",
          "And fear not them which kill the body, but are not able to kill the soul: but rather fear him which is able to destroy both soul and body in hell.",
          "And do not fear those who kill the body but cannot kill the soul. Rather fear him who can destroy both soul and body in hell."),
    ])

    # ── ANXIETY ──
    add_verses(data, 'anxiety', [
        v("Psalms",46,1,2,"Psalms 46:1-2","A psalm of confidence in God's presence and power","c. 1000-400 BC",
          "God is our refuge and strength, a very present help in trouble. Therefore will not we fear, though the earth be removed, and though the mountains be carried into the midst of the sea;",
          "God is our refuge and strength, a very present help in trouble. Therefore we will not fear though the earth gives way, though the mountains be moved into the heart of the sea,"),
        v("Proverbs",12,25,None,"Proverbs 12:25","Solomon on the weight of anxiety and the power of a good word","c. 970-700 BC",
          "Heaviness in the heart of man maketh it stoop: but a good word maketh it glad.",
          "Anxiety in a man's heart weighs him down, but a good word makes him glad."),
        v("Matthew",11,28,30,"Matthew 11:28-30","Jesus inviting the weary to find rest in him","c. 50-70 AD",
          "Come unto me, all ye that labour and are heavy laden, and I will give you rest. Take my yoke upon you, and learn of me; for I am meek and lowly in heart: and ye shall find rest unto your souls. For my yoke is easy, and my burden is light.",
          'Come to me, all who labor and are heavy laden, and I will give you rest. Take my yoke upon you, and learn from me, for I am gentle and lowly in heart, and you will find rest for your souls. For my yoke is easy, and my burden is light."'),
        v("Psalms",139,23,24,"Psalms 139:23-24","David inviting God to search his heart and remove anxiety","c. 1000-400 BC",
          "Search me, O God, and know my heart: try me, and know my thoughts: And see if there be any wicked way in me, and lead me in the way everlasting.",
          "Search me, O God, and know my heart! Try me and know my thoughts! And see if there be any grievous way in me, and lead me in the way everlasting!"),
        v("Lamentations",3,22,23,"Lamentations 3:22-23","Jeremiah finding hope in God's faithfulness amid despair","c. 586 BC",
          "It is of the LORD's mercies that we are not consumed, because his compassions fail not. They are new every morning: great is thy faithfulness.",
          "The steadfast love of the LORD never ceases; his mercies never come to an end; they are new every morning; great is your faithfulness."),
    ])

    # ── ADDICTION ──
    add_verses(data, 'addiction', [
        v("Titus",2,11,12,"Titus 2:11-12","Paul writing to Titus about the grace of God that teaches self-control","c. 63-65 AD",
          "For the grace of God that bringeth salvation hath appeared to all men, Teaching us that, denying ungodliness and worldly lusts, we should live soberly, righteously, and godly, in this present world;",
          "For the grace of God has appeared, bringing salvation for all people, training us to renounce ungodliness and worldly passions, and to live self-controlled, upright, and godly lives in the present age,"),
        v("Philippians",4,13,None,"Philippians 4:13","Paul writing from prison to the believers at Philippi about strength in Christ","c. 61-62 AD",
          "I can do all things through Christ which strengtheneth me.",
          "I can do all things through him who strengthens me."),
        v("Psalms",107,13,14,"Psalms 107:13-14","A psalm celebrating God's deliverance of those in bondage","c. 1000-400 BC",
          "Then they cried unto the LORD in their trouble, and he saved them out of their distresses. He brought them out of darkness and the shadow of death, and brake their bands in sunder.",
          "Then they cried to the LORD in their trouble, and he delivered them from their distress. He brought them out of darkness and the shadow of death, and burst their bonds apart."),
        v("James",4,7,None,"James 4:7","James, brother of Jesus, on resisting the devil","c. 45-49 AD",
          "Submit yourselves therefore to God. Resist the devil, and he will flee from you.",
          "Submit yourselves therefore to God. Resist the devil, and he will flee from you."),
        v("Proverbs",23,29,32,"Proverbs 23:29-32","Solomon's vivid warning against the bondage of strong drink","c. 970-700 BC",
          "Who hath woe? who hath sorrow? who hath contentions? who hath babbling? who hath wounds without cause? who hath redness of eyes? They that tarry long at the wine; they that go to seek mixed wine. Look not thou upon the wine when it is red, when it giveth his colour in the cup, when it moveth itself aright. At the last it biteth like a serpent, and stingeth like an adder.",
          "Who has woe? Who has sorrow? Who has strife? Who has complaining? Who has wounds without cause? Who has redness of eyes? Those who tarry long over wine; those who go to try mixed wine. Do not look at wine when it is red, when it sparkles in the cup and goes down smoothly. In the end it bites like a serpent and stings like an adder."),
        v("1 Peter",5,8,None,"1 Peter 5:8","Peter warning the scattered believers to be vigilant","c. 64-65 AD",
          "Be sober, be vigilant; because your adversary the devil, as a roaring lion, walketh about, seeking whom he may devour:",
          "Be sober-minded; be watchful. Your adversary the devil prowls around like a roaring lion, seeking someone to devour."),
    ])

    # ── LIES & DECEPTION ──
    add_verses(data, 'lies-deception', [
        v("Proverbs",6,16,19,"Proverbs 6:16-19","Solomon listing the things the Lord hates","c. 970-700 BC",
          "These six things doth the LORD hate: yea, seven are an abomination unto him: A proud look, a lying tongue, and hands that shed innocent blood, An heart that deviseth wicked imaginations, feet that be swift in running to mischief, A false witness that speaketh lies, and he that soweth discord among brethren.",
          "There are six things that the LORD hates, seven that are an abomination to him: haughty eyes, a lying tongue, and hands that shed innocent blood, a heart that devises wicked plans, feet that make haste to run to evil, a false witness who breathes out lies, and one who sows discord among brothers."),
        v("Psalms",34,13,None,"Psalms 34:13","David instructing on keeping the tongue from evil","c. 1000-400 BC",
          "Keep thy tongue from evil, and thy lips from speaking guile.",
          "Keep your tongue from evil and your lips from speaking deceit."),
        v("Exodus",20,16,None,"Exodus 20:16","The ninth commandment given by God to Moses at Sinai","c. 1446 BC",
          "Thou shalt not bear false witness against thy neighbour.",
          "You shall not bear false witness against your neighbor."),
        v("Proverbs",11,3,None,"Proverbs 11:3","Solomon on integrity versus deception","c. 970-700 BC",
          "The integrity of the upright shall guide them: but the perverseness of transgressors shall destroy them.",
          "The integrity of the upright guides them, but the crookedness of the treacherous destroys them."),
        v("Leviticus",19,11,None,"Leviticus 19:11","God commanding Moses regarding honesty among the people","c. 1446 BC",
          "Ye shall not steal, neither deal falsely, neither lie one to another.",
          "You shall not steal; you shall not deal falsely; you shall not lie to one another."),
        v("Proverbs",26,28,None,"Proverbs 26:28","Solomon on the destructive nature of a lying tongue","c. 970-700 BC",
          "A lying tongue hateth those that are afflicted by it; and a flattering mouth worketh ruin.",
          "A lying tongue hates its victims, and a flattering mouth works ruin."),
    ])

    # ── JEALOUSY ──
    add_verses(data, 'jealousy', [
        v("Proverbs",23,17,None,"Proverbs 23:17","Solomon warning against envying sinners","c. 970-700 BC",
          "Let not thine heart envy sinners: but be thou in the fear of the LORD all the day long.",
          "Let not your heart envy sinners, but continue in the fear of the LORD all the day."),
        v("James",3,14,15,"James 3:14-15","James on the source of bitter jealousy","c. 45-49 AD",
          "But if ye have bitter envying and strife in your hearts, glory not, and lie not against the truth. This wisdom descendeth not from above, but is earthly, sensual, devilish.",
          "But if you have bitter jealousy and selfish ambition in your hearts, do not boast and be false to the truth. This is not the wisdom that comes down from above, but is earthly, unspiritual, demonic."),
        v("Psalms",37,1,None,"Psalms 37:1","David instructing against envying evildoers","c. 1000-400 BC",
          "Fret not thyself because of evildoers, neither be thou envious against the workers of iniquity.",
          "Fret not yourself because of evildoers; be not envious of wrongdoers!"),
        v("Ecclesiastes",4,4,None,"Ecclesiastes 4:4","Solomon observing that toil is driven by envy","c. 935 BC",
          "Again, I considered all travail, and every right work, that for this a man is envied of his neighbour. This is also vanity and vexation of spirit.",
          "Then I saw that all toil and all skill in work come from a man's envy of his neighbor. This also is vanity and a striving after wind."),
        v("Galatians",5,19,21,"Galatians 5:19-21","Paul listing the works of the flesh to the assemblies of Galatia","c. 49-55 AD",
          "Now the works of the flesh are manifest, which are these; Adultery, fornication, uncleanness, lasciviousness, Idolatry, witchcraft, hatred, variance, emulations, wrath, strife, seditions, heresies, Envyings, murders, drunkenness, revellings, and such like: of the which I tell you before, as I have also told you in time past, that they which do such things shall not inherit the kingdom of God.",
          "Now the works of the flesh are evident: sexual immorality, impurity, sensuality, idolatry, sorcery, enmity, strife, jealousy, fits of anger, rivalries, dissensions, divisions, envy, drunkenness, orgies, and things like these. I warn you, as I warned you before, that those who do such things will not inherit the kingdom of God."),
    ])

    # ── GRIEF ──
    add_verses(data, 'grief', [
        v("Psalms",30,5,None,"Psalms 30:5","David on the brevity of God's anger and the joy that comes","c. 1000-400 BC",
          "For his anger endureth but a moment; in his favour is life: weeping may endure for a night, but joy cometh in the morning.",
          "For his anger is but for a moment, and his favor is for a lifetime. Weeping may tarry for the night, but joy comes with the morning."),
        v("Isaiah",61,1,3,"Isaiah 61:1-3","Isaiah prophesying comfort for those who mourn in Zion","c. 740-680 BC",
          "The Spirit of the Lord GOD is upon me; because the LORD hath anointed me to preach good tidings unto the meek; he hath sent me to bind up the brokenhearted, to proclaim liberty to the captives, and the opening of the prison to them that are bound; To proclaim the acceptable year of the LORD, and the day of vengeance of our God; to comfort all that mourn; To appoint unto them that mourn in Zion, to give unto them beauty for ashes, the oil of joy for mourning, the garment of praise for the spirit of heaviness; that they might be called trees of righteousness, the planting of the LORD, that he might be glorified.",
          "The Spirit of the Lord GOD is upon me, because the LORD has anointed me to bring good news to the poor; he has sent me to bind up the brokenhearted, to proclaim liberty to the captives, and the opening of the prison to those who are bound; to proclaim the year of the LORD's favor, and the day of vengeance of our God; to comfort all who mourn; to grant to those who mourn in Zion--to give them a beautiful headdress instead of ashes, the oil of gladness instead of mourning, the garment of praise instead of a faint spirit; that they may be called oaks of righteousness, the planting of the LORD, that he may be glorified."),
        v("John",14,1,3,"John 14:1-3","Jesus comforting his disciples before his crucifixion","c. 85-95 AD",
          "Let not your heart be troubled: ye believe in God, believe also in me. In my Father's house are many mansions: if it were not so, I would have told you. I go to prepare a place for you. And if I go and prepare a place for you, I will come again, and receive you unto myself; that where I am, there ye may be also.",
          'Let not your hearts be troubled. Believe in God; believe also in me. In my Father\'s house are many rooms. If it were not so, would I have told you that I go to prepare a place for you? And if I go and prepare a place for you, I will come again and will take you to myself, that where I am you may be also.'),
        v("Lamentations",3,22,23,"Lamentations 3:22-23","Jeremiah finding hope in God's faithfulness amid sorrow","c. 586 BC",
          "It is of the LORD's mercies that we are not consumed, because his compassions fail not. They are new every morning: great is thy faithfulness.",
          "The steadfast love of the LORD never ceases; his mercies never come to an end; they are new every morning; great is your faithfulness."),
    ])

    # ── PRIDE ──
    add_verses(data, 'pride', [
        v("Proverbs",8,13,None,"Proverbs 8:13","Wisdom personified declaring what is hateful to God","c. 970-700 BC",
          "The fear of the LORD is to hate evil: pride, and arrogancy, and the evil way, and the froward mouth, do I hate.",
          "The fear of the LORD is hatred of evil. Pride and arrogance and the way of evil and perverted speech I hate."),
        v("Daniel",4,37,None,"Daniel 4:37","Nebuchadnezzar's testimony after God humbled him","c. 530 BC",
          "Now I Nebuchadnezzar praise and extol and honour the King of heaven, all whose works are truth, and his ways judgment: and those that walk in pride he is able to abase.",
          "Now I, Nebuchadnezzar, praise and extol and honor the King of heaven, for all his works are right and his ways are just; and those who walk in pride he is able to humble."),
        v("Luke",14,11,None,"Luke 14:11","Jesus teaching at a Pharisee's house about humility","c. 60-62 AD",
          "For whosoever exalteth himself shall be abased; and he that humbleth himself shall be exalted.",
          "For everyone who exalts himself will be humbled, and he who humbles himself will be exalted."),
        v("Galatians",6,3,None,"Galatians 6:3","Paul warning the assemblies of Galatia against self-deception","c. 49-55 AD",
          "For if a man think himself to be something, when he is nothing, he deceiveth himself.",
          "For if anyone thinks he is something, when he is nothing, he deceives himself."),
        v("Proverbs",29,23,None,"Proverbs 29:23","Solomon contrasting pride and humility","c. 970-700 BC",
          "A man's pride shall bring him low: but honour shall uphold the humble in spirit.",
          "One's pride will bring him low, but he who is lowly in spirit will obtain honor."),
        v("Isaiah",2,12,None,"Isaiah 2:12","Isaiah prophesying the day of the Lord against the proud","c. 740-680 BC",
          "For the day of the LORD of hosts shall be upon every one that is proud and lofty, and upon every one that is lifted up; and he shall be brought low:",
          "For the LORD of hosts has a day against all that is proud and lofty, against all that is lifted up--and it shall be brought low;"),
    ])

    # ── UNFORGIVENESS ──
    add_verses(data, 'unforgiveness', [
        v("Luke",17,3,4,"Luke 17:3-4","Jesus teaching his disciples about repeated forgiveness","c. 60-62 AD",
          "Take heed to yourselves: If thy brother trespass against thee, rebuke him; and if he repent, forgive him. And if he trespass against thee seven times in a day, and seven times in a day turn again to thee, saying, I repent; thou shalt forgive him.",
          'Pay attention to yourselves! If your brother sins, rebuke him, and if he repents, forgive him, and if he sins against you seven times in the day, and turns to you seven times, saying, "I repent," you must forgive him.'),
        v("2 Corinthians",2,10,11,"2 Corinthians 2:10-11","Paul urging forgiveness to prevent Satan's schemes","c. 56 AD",
          "To whom ye forgive any thing, I forgive also: for if I forgave any thing, to whom I forgave it, for your sakes forgave I it in the person of Christ; Lest Satan should get an advantage of us: for we are not ignorant of his devices.",
          "Anyone whom you forgive, I also forgive. Indeed, what I have forgiven, if I have forgiven anything, has been for your sake in the presence of Christ, so that we would not be outwitted by Satan; for we are not ignorant of his designs."),
        v("Matthew",5,44,None,"Matthew 5:44","Jesus commanding love for enemies in the Sermon on the Mount","c. 50-70 AD",
          "But I say unto you, Love your enemies, bless them that curse you, do good to them that hate you, and pray for them which despitefully use you, and persecute you;",
          "But I say to you, Love your enemies and pray for those who persecute you,"),
        v("Proverbs",19,11,None,"Proverbs 19:11","Solomon on the glory of passing over offenses","c. 970-700 BC",
          "The discretion of a man deferreth his anger; and it is his glory to pass over a transgression.",
          "Good sense makes one slow to anger, and it is his glory to overlook an offense."),
    ])

    # ── DOUBT ──
    add_verses(data, 'doubt', [
        v("Proverbs",3,5,6,"Proverbs 3:5-6","Solomon on trusting the Lord completely","c. 970-700 BC",
          "Trust in the LORD with all thine heart; and lean not unto thine own understanding. In all thy ways acknowledge him, and he shall direct thy paths.",
          "Trust in the LORD with all your heart, and do not lean on your own understanding. In all your ways acknowledge him, and he will make straight your paths."),
        v("Matthew",17,20,None,"Matthew 17:20","Jesus teaching his disciples about the power of faith","c. 50-70 AD",
          "And Jesus said unto them, Because of your unbelief: for verily I say unto you, If ye have faith as a grain of mustard seed, ye shall say unto this mountain, Remove hence to yonder place; and it shall remove; and nothing shall be impossible unto you.",
          'He said to them, "Because of your little faith. For truly, I say to you, if you have faith like a grain of mustard seed, you will say to this mountain, \'Move from here to there,\' and it will move, and nothing will be impossible for you."'),
        v("Luke",1,37,None,"Luke 1:37","The angel Gabriel speaking to Mary","c. 60-62 AD",
          "For with God nothing shall be impossible.",
          "For nothing will be impossible with God."),
        v("2 Corinthians",5,7,None,"2 Corinthians 5:7","Paul on walking by faith to the believers in Corinth","c. 56 AD",
          "(For we walk by faith, not by sight:)",
          "For we walk by faith, not by sight."),
        v("Hebrews",11,6,None,"Hebrews 11:6","The author of Hebrews on the necessity of faith","c. 64-68 AD",
          "But without faith it is impossible to please him: for he that cometh to God must believe that he is, and that he is a rewarder of them that diligently seek him.",
          "And without faith it is impossible to please him, for whoever would draw near to God must believe that he exists and that he rewards those who seek him."),
    ])

    # ── LAZINESS ──
    add_verses(data, 'laziness', [
        v("Proverbs",10,4,None,"Proverbs 10:4","Solomon contrasting lazy and diligent hands","c. 970-700 BC",
          "He becometh poor that dealeth with a slack hand: but the hand of the diligent maketh rich.",
          "A slack hand causes poverty, but the hand of the diligent makes rich."),
        v("Proverbs",20,4,None,"Proverbs 20:4","Solomon on the sluggard who does not plow in season","c. 970-700 BC",
          "The sluggard will not plow by reason of the cold; therefore shall he beg in harvest, and have nothing.",
          "The sluggard does not plow in the autumn; he will seek at harvest and have nothing."),
        v("Romans",12,11,None,"Romans 12:11","Paul urging the believers in Rome to be fervent in spirit","c. 57 AD",
          "Not slothful in business; fervent in spirit; serving the Lord;",
          "Do not be slothful in zeal, be fervent in spirit, serve the Lord."),
        v("1 Corinthians",15,58,None,"1 Corinthians 15:58","Paul encouraging steadfastness and abundance in the Lord's work","c. 55 AD",
          "Therefore, my beloved brethren, be ye stedfast, unmoveable, always abounding in the work of the Lord, forasmuch as ye know that your labour is not in vain in the Lord.",
          "Therefore, my beloved brothers, be steadfast, immovable, always abounding in the work of the Lord, knowing that in the Lord your labor is not in vain."),
        v("Proverbs",18,9,None,"Proverbs 18:9","Solomon on the kinship between sloth and destruction","c. 970-700 BC",
          "He also that is slothful in his work is brother to him that is a great waster.",
          "Whoever is slack in his work is a brother to him who destroys."),
    ])

    # Save
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    total = sum(len(c['verses']) for c in data['categories'])
    print(f"Total: {total} verses across {len(data['categories'])} categories")
    for c in data['categories']:
        print(f"  {c['slug']:30s} {len(c['verses'])} verses")

if __name__ == '__main__':
    main()
