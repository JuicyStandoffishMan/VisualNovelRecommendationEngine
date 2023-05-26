# Visual Novel Recommendation Engine
A simple visual novel recommendation engine using VNDB data dumps.

## Quickstart
Follow these steps to just get recommendations on Windows. Linux/Mac users, YOYO, but it should be similar.

**Make sure you have Python installed:**

https://www.python.org/downloads/

**Clone this repository:**
```bash
git clone https://github.com/JuicyStandoffishMan/VisualNovelRecommendationEngine.git
cd VisualNovelRecommendationEngine
```

**(Optional) Create a virtual environment:**
```
python -m venv env
.\env\Scripts\activate
```

**Install the dependencies:**
```
pip install -r requirements.txt
```

(Optional) Alternatively, if you want to use `vnrec.py` as a lib, run:
```
python setup.py install
```

**Execute test.py:**
```
python test.py
```

You should see some loading messages, followed by a prompt to enter the VN(DB) ID. Note that it will take a while to calculate the tag similarity matrix.
```
Loading titles
Loading votes
Calculating average ratings
Loading tags_vn
Building average tags
Calculating tag similarity matrix.
Similarity matrix computed.
Loading complete.

Enter the VN_ID: 
```

VN_ID is the VNDB id (**without** the leading v). For example, https://vndb.org/v7771 would be **7771**.

## Using VNDB Data Dumps
This library stores the necessary dumps as of **May 26, 2023**, but you can always update them manually by visiting [VNDB's Data Dumps](https://vndb.org/d14). Make sure the votes file is renamed to `votes`. The other files can be pulled out of the `db` folder from the nearly-complete database download. Place them in the local `data` folder.

## API Usage
```python
from vnrec import vn

engine = vn()
vn_id = 7771

top_votes = engine.get_user_recommendations(vn_id)
top_tags = engine.get_tag_recommendations(vn_id)
top_combined = engine.get_combined_recommendations(vn_id)
```

Alternatively, there are `_score` suffixes to the above which return not just the IDs of the VNs, but also their normalized scores.

### Ignored tags
There are tags ignored in the tag scoring, and is currently not at all exhaustive. It just uses some presentation ones, like ADV and NVL.
```python
self.ignore_tags = [32, 2040, 2461, 1434, 1431, 43]
```

## How it works
There are 2 scoring systems:
- **User votes:** Gives a "people also liked". It only looks at the public votes supplied by VNDB, as anonymous votes are not available, and applies `vote_exp` **pre-average**.
- **Similar tags:** Gives a "visual novel like" by using non-zero tag weights. The library will average out all of the tag votes **after** applying `tag-exp` to their weights (while keeping the sign).

A very basic combination scoring system using weighted summation (`vote_weight` and `tag_weight` is also available). `tag_weight` defaults to 1.5 because the vote score tends to dominate and just give the most popular VNs.

## Credits and License
This repo is MIT. See [VNDB's data license](https://vndb.org/d17#4) as well.

Huge shoutout to ChatGPT for writing most of the code and answering all my questions along the way.

## Examples
### White Album 2 Closing Chapter
```
Enter the VN_ID: 7771
Recommendations for WHITE ALBUM 2 ~closing chapter~:
Votes (1.0):
{
        1. WHITE ALBUM 2 ~introductory chapter~ (2920)
        2. Muv-Luv Alternative (92)
        3. Fate/stay night (11)
        4. Steins;Gate (2002)
        5. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
        6. The Fruit of Grisaia (5154)
        7. G-senjou no Maou - The Devil on G-String (211)
        8. Saya no Uta ~ The Song of Saya (97)
        9. CLANNAD (4)
        10. Umineko When They Cry - Question Arcs (24)
        11. Little Busters! (5)
        12. Muv-Luv (93)
        13. Rewrite (751)
        14. Full Metal Daemon Muramasa (2016)
        15. Umineko When They Cry - Answer Arcs (2153)
        16. Majikoi! Love Me Seriously!! (1143)
        17. Aokana -Four Rhythms Across the Blue- (12849)
        18. Ever17 -out of infinity- (17)
        19. BALDR SKY Dive2 "RECORDARE" (1913)
        20. BALDR SKY Dive1 "Lost Memory" (1306)
        21. Tsukihime (7)
        22. The House in Fata Morgana (12402)
        23. Sharin no Kuni: The Girl Among the Sunflowers (57)
        24. Kara no Shojo (810)
        25. YOU and ME and HER: A Love Story (7738)
}

Tags (1.5):
{
        1. WHITE ALBUM (236)
        2. December when there is no angel (21)
        3. Tomoyo After ~It's a Wonderful Life~ (12)
        4. Reversible (1416)
        5. Gin'iro, Haruka (18778)
        6. Night Strangers (39677)
        7. Free Love (10292)
        8. WHITE ALBUM 2 ~introductory chapter~ (2920)
        9. Kimi ga Ita Kisetsu (443)
        10. Ore to Osananajimi no Hateshinai Ecchi Battle (38403)
        11. The Scrum Of It All (44501)
        12. Kromka (30207)
        13. Yome no Imouto to H na Kankei ni Natte Yabai!? (28332)
        14. The Most Forbidden Love in the World (415)
        15. L (8378)
        16. Koi de wa Naku - It's not love, but so where near. (5746)
        17. Azazel (7658)
        18. Hoshi Ori Yume Mirai (14265)
        19. Koisuru Natsu no Last Resort (13046)
        20. Biniku no Kaori - Bangai Hen (10992)
        21. Enkyori Kanojo to Kinkyori Hime (21689)
        22. Sumire no Tsubomi Fan Disc ~Wedding Daisakusen~ (2988)
        23. Koi x Shin Ai Kanojo (17516)
        24. Sakura no Niwa (11481)
        25. Ore wa Kanojo o Shinjiteru! ~Enkyori Ren'ai no Susume~ (495)
}

Combined:
{
        1. WHITE ALBUM (236)
        2. WHITE ALBUM 2 ~introductory chapter~ (2920)
        3. December when there is no angel (21)
        4. Tomoyo After ~It's a Wonderful Life~ (12)
        5. Muv-Luv Alternative (92)
        6. Fate/stay night (11)
        7. Steins;Gate (2002)
        8. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
        9. Reversible (1416)
        10. Gin'iro, Haruka (18778)
        11. Night Strangers (39677)
        12. The Fruit of Grisaia (5154)
        13. G-senjou no Maou - The Devil on G-String (211)
        14. Free Love (10292)
        15. Saya no Uta ~ The Song of Saya (97)
        16. Kimi ga Ita Kisetsu (443)
        17. Ore to Osananajimi no Hateshinai Ecchi Battle (38403)
        18. The Scrum Of It All (44501)
        19. Kromka (30207)
        20. Yome no Imouto to H na Kankei ni Natte Yabai!? (28332)
        21. CLANNAD (4)
        22. Umineko When They Cry - Question Arcs (24)
        23. Little Busters! (5)
        24. Muv-Luv (93)
        25. Rewrite (751)
}
```

### Fruit of Grisaia
```
Enter the VN_ID: 5154
Recommendations for The Fruit of Grisaia:
Votes (1.0):
{
        1. G-senjou no Maou - The Devil on G-String (211)
        2. Fate/stay night (11)
        3. Katawa Shoujo (945)
        4. Steins;Gate (2002)
        5. Majikoi! Love Me Seriously!! (1143)
        6. Muv-Luv Alternative (92)
        7. Saya no Uta ~ The Song of Saya (97)
        8. The Labyrinth of Grisaia (7723)
        9. Little Busters! (5)
        10. CLANNAD (4)
        11. Rewrite (751)
        12. Muv-Luv (93)
        13. Sharin no Kuni: The Girl Among the Sunflowers (57)
        14. The Eden of Grisaia (7724)
        15. Danganronpa: Trigger Happy Havoc (7014)
        16. Hoshizora no Memoria -Wish upon a Shooting Star- (1474)
        17. Umineko When They Cry - Question Arcs (24)
        18. If My Heart Had Wings (9093)
        19. Maji de Watashi ni Koishinasai! S (6245)
        20. Tsukihime (7)
        21. Danganronpa 2: Goodbye Despair (7679)
        22. Doki Doki Literature Club! (21905)
        23. Ever17 -out of infinity- (17)
        24. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
        25. Umineko When They Cry - Answer Arcs (2153)
}

Tags (1.5):
{
        1. The Labyrinth of Grisaia (7723)
        2. Amakano (15679)
        3. Princess Evangile (6710)
        4. Kotowari ~Kimi no Kokoro no Koboreta Kakera~ (6918)
        5. The Eden of Grisaia (7724)
        6. Saku Saku: Love Blooms with the Cherry Blossoms (10304)
        7. Tsujidou-san no Jun'ai Road (9879)
        8. Koi Iro Marriage (10396)
        9. A Sky Full of Stars (16560)
        10. Yukikoi Melt (15064)
        11. Lovesick Puppies -Bokura wa Koi Suru Tame ni Umaretekita- (11194)
        12. Daitoshokan no Hitsujikai (8158)
        13. Nursery☆Rhyme (310)
        14. If My Heart Had Wings -Flight Diary- (10979)
        15. Amenity's Life (19609)
        16. Noble ☆ Works (4806)
        17. Hatsukoi Time Capsule ~Osananajimi to Kya Kya Ufufu~ (4065)
        18. Yumeiro Alouette! (9127)
        19. Mashiro-iro Symphony (1552)
        20. Ikinari Anata ni Koishiteiru (5240)
        21. Daitoshokan no Hitsujikai -Dreaming Sheep- (12480)
        22. Akiyume Kukuru (15744)
        23. Itoshii Kanojo no Mamorikata (6242)
        24. Himawari no Kyoukai to Nagai Natsuyasumi (10557)
        25. Hoshi Ori Yume Mirai (14265)
}

Combined:
{
        1. The Labyrinth of Grisaia (7723)
        2. Amakano (15679)
        3. G-senjou no Maou - The Devil on G-String (211)
        4. Fate/stay night (11)
        5. The Eden of Grisaia (7724)
        6. Katawa Shoujo (945)
        7. Princess Evangile (6710)
        8. Steins;Gate (2002)
        9. Majikoi! Love Me Seriously!! (1143)
        10. Kotowari ~Kimi no Kokoro no Koboreta Kakera~ (6918)
        11. Muv-Luv Alternative (92)
        12. Saya no Uta ~ The Song of Saya (97)
        13. Little Busters! (5)
        14. CLANNAD (4)
        15. Rewrite (751)
        16. Saku Saku: Love Blooms with the Cherry Blossoms (10304)
        17. Tsujidou-san no Jun'ai Road (9879)
        18. Koi Iro Marriage (10396)
        19. A Sky Full of Stars (16560)
        20. Muv-Luv (93)
        21. Yukikoi Melt (15064)
        22. Sharin no Kuni: The Girl Among the Sunflowers (57)
        23. Lovesick Puppies -Bokura wa Koi Suru Tame ni Umaretekita- (11194)
        24. Daitoshokan no Hitsujikai (8158)
        25. Nursery☆Rhyme (310)
}
```

### Clannad
```
Enter the VN_ID: 4
Recommendations for CLANNAD:
Votes (1.0):
{
        1. Fate/stay night (11)
        2. Steins;Gate (2002)
        3. Little Busters! (5)
        4. G-senjou no Maou - The Devil on G-String (211)
        5. Katawa Shoujo (945)
        6. Saya no Uta ~ The Song of Saya (97)
        7. The Fruit of Grisaia (5154)
        8. Rewrite (751)
        9. Muv-Luv Alternative (92)
        10. Umineko When They Cry - Question Arcs (24)
        11. Ever17 -out of infinity- (17)
        12. Tsukihime (7)
        13. planetarian ~Dream of Little Star~ (34)
        14. Sharin no Kuni: The Girl Among the Sunflowers (57)
        15. Majikoi! Love Me Seriously!! (1143)
        16. Muv-Luv (93)
        17. Danganronpa: Trigger Happy Havoc (7014)
        18. Higurashi When They Cry - Question Arcs (67)
        19. Umineko When They Cry - Answer Arcs (2153)
        20. Kanon (33)
        21. Danganronpa 2: Goodbye Despair (7679)
        22. Doki Doki Literature Club! (21905)
        23. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
        24. Chaos;Head (382)
        25. Higurashi When They Cry - Answer Arcs (68)
}

Tags (1.5):
{
        1. Little Busters! (5)
        2. Koi x Shin Ai Kanojo (17516)
        3. Fragment's Note 2 Side: Yukitsuki (14807)
        4. Kanon (33)
        5. Fragment's Note 2 Side: Shizuku (13119)
        6. Clannad -The Past Path- (7983)
        7. Crescendo (29)
        8. Flyable Heart (1179)
        9. Tokyo ReConnect (24599)
        10. AIR (36)
        11. Memories Off (1152)
        12. Brass Restoration (167)
        13. Hoshizora no Memoria -Wish upon a Shooting Star- (1474)
        14. Summer Pockets (20424)
        15. Hare Nochi Kitto Nanohana Biyori (14886)
        16. Hope~ Symphony of Tomorrow (10845)
        17. Saku Saku: Love Blooms with the Cherry Blossoms (10304)
        18. ONE ~To the Radiant Season~ (51)
        19. Majikoi! Love Me Seriously!! (1143)
        20. ToHeart2 (20)
        21. Rewrite (751)
        22. Yoake Mae yori Ruri Iro na (232)
        23. deIz (7816)
        24. Doki Doki Literature Club! Purist Mod (25414)
        25. Symphonic Rain (38)
}

Combined:
{
        1. Little Busters! (5)
        2. Koi x Shin Ai Kanojo (17516)
        3. Fragment's Note 2 Side: Yukitsuki (14807)
        4. Kanon (33)
        5. Fragment's Note 2 Side: Shizuku (13119)
        6. Clannad -The Past Path- (7983)
        7. Fate/stay night (11)
        8. Crescendo (29)
        9. Flyable Heart (1179)
        10. Tokyo ReConnect (24599)
        11. Steins;Gate (2002)
        12. AIR (36)
        13. Memories Off (1152)
        14. Brass Restoration (167)
        15. Rewrite (751)
        16. G-senjou no Maou - The Devil on G-String (211)
        17. Hoshizora no Memoria -Wish upon a Shooting Star- (1474)
        18. Katawa Shoujo (945)
        19. Saya no Uta ~ The Song of Saya (97)
        20. The Fruit of Grisaia (5154)
        21. Summer Pockets (20424)
        22. Majikoi! Love Me Seriously!! (1143)
        23. Muv-Luv Alternative (92)
        24. Hare Nochi Kitto Nanohana Biyori (14886)
        25. Hope~ Symphony of Tomorrow (10845)
}
```

### Aokana
```
Enter the VN_ID: 12849
Recommendations for Aokana -Four Rhythms Across the Blue-:
Votes (1.0):
{
        1. The Fruit of Grisaia (5154)
        2. Sabbat of the Witch (16044)
        3. Senren＊Banka (19073)
        4. Majikoi! Love Me Seriously!! (1143)
        5. G-senjou no Maou - The Devil on G-String (211)
        6. Steins;Gate (2002)
        7. RIDDLE JOKER (22230)
        8. Fate/stay night (11)
        9. If My Heart Had Wings (9093)
        10. Kinkoi: Golden Loveriche (21852)
        11. Making * Lovers (21552)
        12. Muv-Luv Alternative (92)
        13. Summer Pockets (20424)
        14. Little Busters! (5)
        15. Saya no Uta ~ The Song of Saya (97)
        16. Rewrite (751)
        17. 9-nine-:Episode 2 (21668)
        18. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
        19. The Labyrinth of Grisaia (7723)
        20. 9-nine-:Episode 1 (19829)
        21. Katawa Shoujo (945)
        22. CLANNAD (4)
        23. 9-nine-:Episode 4 (26523)
        24. Hoshizora no Memoria -Wish upon a Shooting Star- (1474)
        25. 9-nine-:Episode 3 (23740)
}

Tags (1.5):
{
        1. Aokana - Four Rhythms Across the Blue - EXTRA2 (21438)
        2. Sora ni Kizanda Parallelogram (23908)
        3. Daitoshokan no Hitsujikai (8158)
        4. Sabbat of the Witch (16044)
        5. If My Heart Had Wings (9093)
        6. A Sky Full of Stars (16560)
        7. Hatsukoi 1/1 (9124)
        8. Hoshi Ori Yume Mirai (14265)
        9. Kimi no Tonari de Koishiteru! (15870)
        10. Lovesick Puppies -Bokura wa Koi Suru Tame ni Umaretekita- (11194)
        11. Princess Evangile (6710)
        12. Himegoto Union ~We Are in the Springtime of Life!~ (12437)
        13. Amakano (15679)
        14. Love, Elections, & Chocolate (4028)
        15. Gangsta Republica (11204)
        16. Little Princess's Serenade (11072)
        17. Koiiro Soramoyou (1740)
        18. W. L. O. Sekai Ren'ai Kikou (1181)
        19. Farther Than the Blue Sky (15077)
        20. Suiheisen made Nan Mile? - Deep Blue Sky & Pure White Wings - (972)
        21. Majikoi! Love Me Seriously!! (1143)
        22. Maji de Watashi ni Koishinasai! S (6245)
        23. Maji de Watashi ni Koishinasai! A-1 (20598)
        24. Honey Coming (180)
        25. Cocoro@Function! (12561)
}

Combined:
{
        1. Sabbat of the Witch (16044)
        2. Aokana - Four Rhythms Across the Blue - EXTRA2 (21438)
        3. Sora ni Kizanda Parallelogram (23908)
        4. If My Heart Had Wings (9093)
        5. Daitoshokan no Hitsujikai (8158)
        6. The Fruit of Grisaia (5154)
        7. Majikoi! Love Me Seriously!! (1143)
        8. Senren＊Banka (19073)
        9. A Sky Full of Stars (16560)
        10. Hatsukoi 1/1 (9124)
        11. G-senjou no Maou - The Devil on G-String (211)
        12. Hoshi Ori Yume Mirai (14265)
        13. Steins;Gate (2002)
        14. Kimi no Tonari de Koishiteru! (15870)
        15. RIDDLE JOKER (22230)
        16. Fate/stay night (11)
        17. Lovesick Puppies -Bokura wa Koi Suru Tame ni Umaretekita- (11194)
        18. Princess Evangile (6710)
        19. Himegoto Union ~We Are in the Springtime of Life!~ (12437)
        20. Kinkoi: Golden Loveriche (21852)
        21. Amakano (15679)
        22. Making * Lovers (21552)
        23. Love, Elections, & Chocolate (4028)
        24. Muv-Luv Alternative (92)
        25. Gangsta Republica (11204)
}
```

### Saya no Uta
```
Recommendations for Saya no Uta ~ The Song of Saya:
Votes (1.0):
{
        1. Fate/stay night (11)
        2. Steins;Gate (2002)
        3. Katawa Shoujo (945)
        4. Umineko When They Cry - Question Arcs (24)
        5. G-senjou no Maou - The Devil on G-String (211)
        6. Muv-Luv Alternative (92)
        7. Tsukihime (7)
        8. Danganronpa: Trigger Happy Havoc (7014)
        9. Ever17 -out of infinity- (17)
        10. The Fruit of Grisaia (5154)
        11. Umineko When They Cry - Answer Arcs (2153)
        12. Doki Doki Literature Club! (21905)
        13. Higurashi When They Cry - Question Arcs (67)
        14. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
        15. CLANNAD (4)
        16. planetarian ~Dream of Little Star~ (34)
        17. Muv-Luv (93)
        18. Danganronpa 2: Goodbye Despair (7679)
        19. Kara no Shojo (810)
        20. Little Busters! (5)
        21. 999: Nine Hours, Nine Persons, Nine Doors (3112)
        22. Sharin no Kuni: The Girl Among the Sunflowers (57)
        23. Rewrite (751)
        24. Higurashi When They Cry - Answer Arcs (68)
        25. Phoenix Wright: Ace Attorney (711)
}

Tags (1.5):
{
        1. Saya no Uta - Derangement (22591)
        2. sweet pool (1399)
        3. 3M -Marionettes manipulate the marionette- (5047)
        4. SWAN SONG (914)
        5. Tenpura! -Momiji Oroshi- (16165)
        6. Maggot baits (18077)
        7. Mister Average (13246)
        8. Tsui no Sora Remake (28806)
        9. Yandere (1303)
        10. Chakku! Tsuiteru!! (2119)
        11. Hotaru Yuki (15453)
        12. CAGE -OPEN- (10694)
        13. Shizuku (235)
        14. Kyojin-tachi (19216)
        15. Divi-Dead (119)
        16. Atsui kara (15663)
        17. Danshikou de Atta Kowai Hanashi (29319)
        18. PigeonBlood (10773)
        19. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
        20. Donor (5395)
        21. Sakamichi (16219)
        22. Yumemi Melancholy (31430)
        23. Jisatsu no Tame no 101 no Houhou (6475)
        24. Echo (18157)
        25. The world to reverse. (287)
}

Combined:
{
        1. Saya no Uta - Derangement (22591)
        2. Fate/stay night (11)
        3. Steins;Gate (2002)
        4. Katawa Shoujo (945)
        5. Umineko When They Cry - Question Arcs (24)
        6. G-senjou no Maou - The Devil on G-String (211)
        7. Muv-Luv Alternative (92)
        8. Tsukihime (7)
        9. sweet pool (1399)
        10. Danganronpa: Trigger Happy Havoc (7014)
        11. Ever17 -out of infinity- (17)
        12. The Fruit of Grisaia (5154)
        13. Umineko When They Cry - Answer Arcs (2153)
        14. 3M -Marionettes manipulate the marionette- (5047)
        15. Doki Doki Literature Club! (21905)
        16. Higurashi When They Cry - Question Arcs (67)
        17. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
        18. CLANNAD (4)
        19. SWAN SONG (914)
        20. planetarian ~Dream of Little Star~ (34)
        21. Muv-Luv (93)
        22. Danganronpa 2: Goodbye Despair (7679)
        23. Tenpura! -Momiji Oroshi- (16165)
        24. Kara no Shojo (810)
        25. Maggot baits (18077)
}
```

### Muv-Luv Alternative
```
Enter the VN_ID: 92
Recommendations for Muv-Luv Alternative:
Votes (1.0):
{
        1. Muv-Luv (93)
        2. Fate/stay night (11)
        3. Steins;Gate (2002)
        4. G-senjou no Maou - The Devil on G-String (211)
        5. Saya no Uta ~ The Song of Saya (97)
        6. The Fruit of Grisaia (5154)
        7. Umineko When They Cry - Question Arcs (24)
        8. Umineko When They Cry - Answer Arcs (2153)
        9. Katawa Shoujo (945)
        10. Little Busters! (5)
        11. CLANNAD (4)
        12. Ever17 -out of infinity- (17)
        13. Tsukihime (7)
        14. Rewrite (751)
        15. Majikoi! Love Me Seriously!! (1143)
        16. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
        17. Sharin no Kuni: The Girl Among the Sunflowers (57)
        18. Danganronpa: Trigger Happy Havoc (7014)
        19. Danganronpa 2: Goodbye Despair (7679)
        20. Higurashi When They Cry - Question Arcs (67)
        21. planetarian ~Dream of Little Star~ (34)
        22. Kara no Shojo (810)
        23. 999: Nine Hours, Nine Persons, Nine Doors (3112)
        24. Utawarerumono (3)
        25. Chaos;Head (382)
}

Tags (1.5):
{
        1. Muv-Luv Alternative: Total Eclipse (7052)
        2. Muv-Luv (93)
        3. Schwarzesmarken (14910)
        4. Muv-Luv Unlimited: The Day After (4463)
        5. BALDR SKY Dive2 "RECORDARE" (1913)
        6. ef - a fairy tale of the two. (88)
        7. BALDR SKY Dive1 "Lost Memory" (1306)
        8. Eve of the 12th Month (12562)
        9. Ayu Mayu Alternative (1362)
        10. Steins;Gate (2002)
        11. Muv-Luv Resonative (30412)
        12. Owaru Sekai to Birthday (9196)
        13. Sunrider: Liberation Day (17694)
        14. Tokyo Alice (3684)
        15. Sousei Kitan Aerial (10447)
        16. The Sekimeiya: Spun Glass (29144)
        17. Saiaku Naru Saiyaku Ningen ni Sasagu (23077)
        18. Einstein Yori Ai o Komete: Apollo Crisis (31436)
        19. STEINS;GATE 0 (17102)
        20. Retrocausality (43337)
        21. Natsu no Owari no Nirvana (11193)
        22. Baldr Sky "Zero" (10833)
        23. Zwei Worter (292)
        24. BETA-SIXDOUZE (28326)
        25. J.Q.V Jinrui Kyuusai-bu ~With Love from Isotope~ (10575)
}

Combined:
{
        1. Muv-Luv (93)
        2. Muv-Luv Alternative: Total Eclipse (7052)
        3. Schwarzesmarken (14910)
        4. Steins;Gate (2002)
        5. Fate/stay night (11)
        6. Muv-Luv Unlimited: The Day After (4463)
        7. G-senjou no Maou - The Devil on G-String (211)
        8. Saya no Uta ~ The Song of Saya (97)
        9. BALDR SKY Dive2 "RECORDARE" (1913)
        10. ef - a fairy tale of the two. (88)
        11. The Fruit of Grisaia (5154)
        12. Umineko When They Cry - Question Arcs (24)
        13. BALDR SKY Dive1 "Lost Memory" (1306)
        14. Eve of the 12th Month (12562)
        15. Umineko When They Cry - Answer Arcs (2153)
        16. Katawa Shoujo (945)
        17. Little Busters! (5)
        18. CLANNAD (4)
        19. Ayu Mayu Alternative (1362)
        20. Ever17 -out of infinity- (17)
        21. Tsukihime (7)
        22. Rewrite (751)
        23. Muv-Luv Resonative (30412)
        24. Majikoi! Love Me Seriously!! (1143)
        25. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
}
```

### Umineko
```
Enter the VN_ID: 24
Recommendations for Umineko When They Cry - Question Arcs:
Votes (1.0):
{
        1. Umineko When They Cry - Answer Arcs (2153)
        2. Fate/stay night (11)
        3. Higurashi When They Cry - Question Arcs (67)
        4. Saya no Uta ~ The Song of Saya (97)
        5. Steins;Gate (2002)
        6. Higurashi When They Cry - Answer Arcs (68)
        7. Muv-Luv Alternative (92)
        8. Danganronpa: Trigger Happy Havoc (7014)
        9. Danganronpa 2: Goodbye Despair (7679)
        10. Tsukihime (7)
        11. G-senjou no Maou - The Devil on G-String (211)
        12. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
        13. Ever17 -out of infinity- (17)
        14. 999: Nine Hours, Nine Persons, Nine Doors (3112)
        15. Muv-Luv (93)
        16. Phoenix Wright: Ace Attorney (711)
        17. CLANNAD (4)
        18. Katawa Shoujo (945)
        19. The House in Fata Morgana (12402)
        20. The Fruit of Grisaia (5154)
        21. Little Busters! (5)
        22. Rewrite (751)
        23. Doki Doki Literature Club! (21905)
        24. Danganronpa V3: Killing Harmony (18334)
        25. Phoenix Wright: Ace Attorney - Trials and Tribulations (716)
}

Tags (1.5):
{
        1. Umineko When They Cry - Answer Arcs (2153)
        2. Higurashi When They Cry - Question Arcs (67)
        3. Higurashi When They Cry - Answer Arcs (68)
        4. Noblelige! (5245)
        5. Witches & Woodlands (5055)
        6. Higurashi When They Cry - Console Arcs (31157)
        7. From the Bottom of the Heart (1290)
        8. Umineko no Naku Koro ni Saku (23407)
        9. Umineko no Naku Koro ni Tsubasa (5691)
        10. Danganronpa V3: Killing Harmony (18334)
        11. Higanbana no Saku Yoru ni - The First Night (7576)
        12. Danganronpa 2: Goodbye Despair (7679)
        13. fault - StP - LIGHTKRAVTE (36650)
        14. Trianthology ~Sanmenkyou no Kuni no Alice~ (17136)
        15. Beyond the Boundary (15990)
        16. Umineko no Naku Koro ni Hane (9047)
        17. Danganronpa: Trigger Happy Havoc (7014)
        18. Shinkyoku Soukai Polyphonica ~Farewell Song~ (7727)
        19. Fushigi no Kuni no Kanojo (12650)
        20. The Evil Magician (15719)
        21. EMMA The Story (23062)
        22. Demon and Heart (21478)
        23. Higurashi no Naku Koro ni Hou (15523)
        24. Danganronpa Another: Another Despair Academy (31661)
        25. Witch on the Holy Night (777)
}

Combined:
{
        1. Umineko When They Cry - Answer Arcs (2153)
        2. Higurashi When They Cry - Question Arcs (67)
        3. Higurashi When They Cry - Answer Arcs (68)
        4. Fate/stay night (11)
        5. Saya no Uta ~ The Song of Saya (97)
        6. Steins;Gate (2002)
        7. Danganronpa 2: Goodbye Despair (7679)
        8. Danganronpa: Trigger Happy Havoc (7014)
        9. Noblelige! (5245)
        10. Witches & Woodlands (5055)
        11. Muv-Luv Alternative (92)
        12. Higurashi When They Cry - Console Arcs (31157)
        13. Tsukihime (7)
        14. From the Bottom of the Heart (1290)
        15. Danganronpa V3: Killing Harmony (18334)
        16. Umineko no Naku Koro ni Saku (23407)
        17. G-senjou no Maou - The Devil on G-String (211)
        18. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
        19. Umineko no Naku Koro ni Tsubasa (5691)
        20. Ever17 -out of infinity- (17)
        21. Higanbana no Saku Yoru ni - The First Night (7576)
        22. 999: Nine Hours, Nine Persons, Nine Doors (3112)
        23. fault - StP - LIGHTKRAVTE (36650)
        24. Muv-Luv (93)
        25. Phoenix Wright: Ace Attorney (711)
}
```

### Doki Doki Literature Club
```
Enter the VN_ID: 21905
Recommendations for Doki Doki Literature Club!:
Votes (1.0):
{
        1. Saya no Uta ~ The Song of Saya (97)
        2. Steins;Gate (2002)
        3. Katawa Shoujo (945)
        4. Danganronpa: Trigger Happy Havoc (7014)
        5. Danganronpa 2: Goodbye Despair (7679)
        6. Fate/stay night (11)
        7. Umineko When They Cry - Question Arcs (24)
        8. Higurashi When They Cry - Question Arcs (67)
        9. Umineko When They Cry - Answer Arcs (2153)
        10. The Fruit of Grisaia (5154)
        11. Danganronpa V3: Killing Harmony (18334)
        12. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
        13. Muv-Luv Alternative (92)
        14. 999: Nine Hours, Nine Persons, Nine Doors (3112)
        15. CLANNAD (4)
        16. Phoenix Wright: Ace Attorney (711)
        17. G-senjou no Maou - The Devil on G-String (211)
        18. Higurashi When They Cry - Answer Arcs (68)
        19. Tsukihime (7)
        20. Muv-Luv (93)
        21. STEINS;GATE 0 (17102)
        22. The House in Fata Morgana (12402)
        23. planetarian ~Dream of Little Star~ (34)
        24. Little Busters! (5)
        25. YOU and ME and HER: A Love Story (7738)
}

Tags (1.5):
{
        1. Doki Doki Literature Club! Purist Mod (25414)
        2. Doki Doki 4chan Club! (29269)
        3. Doki Doki! RainClouds (22637)
        4. YOU and ME and HER: A Love Story (7738)
        5. Senpai, Please Look At Me! (31331)
        6. Menherafflesia (22205)
        7. Yumemi Melancholy (31430)
        8. Harem Tengoku da to Omottara Yandere Jigoku Datta. (14536)
        9. Doki Doki: Encore! (36186)
        10. Dice Psycho (29067)
        11. Doki Doki Blue Skies (28556)
        12. Chigau!!! (31573)
        13. Our Love (23046)
        14. Test Gaeshi (35695)
        15. Owaru Sekai to Birthday (9196)
        16. Nothing is Beautiful. (26715)
        17. High school Life: HSL (19551)
        18. Azrael (1831)
        19. Yandere-Chan (10665)
        20. Ushinawareta Mirai o Motomete (4880)
        21. Under The Scarlet Tree! (39227)
        22. The Girl With Vacant Eyes (26720)
        23. Koi Hai Tunnel (31671)
        24. Crimson Gray (21499)
        25. Daitoshokan no Hitsujikai ~Houkago Shippo Days~ (12600)
}

Combined:
{
        1. Doki Doki Literature Club! Purist Mod (25414)
        2. Doki Doki 4chan Club! (29269)
        3. Saya no Uta ~ The Song of Saya (97)
        4. Steins;Gate (2002)
        5. Katawa Shoujo (945)
        6. Danganronpa: Trigger Happy Havoc (7014)
        7. Doki Doki! RainClouds (22637)
        8. Danganronpa 2: Goodbye Despair (7679)
        9. Fate/stay night (11)
        10. YOU and ME and HER: A Love Story (7738)
        11. Umineko When They Cry - Question Arcs (24)
        12. Senpai, Please Look At Me! (31331)
        13. Menherafflesia (22205)
        14. Higurashi When They Cry - Question Arcs (67)
        15. Yumemi Melancholy (31430)
        16. Umineko When They Cry - Answer Arcs (2153)
        17. The Fruit of Grisaia (5154)
        18. Harem Tengoku da to Omottara Yandere Jigoku Datta. (14536)
        19. Doki Doki: Encore! (36186)
        20. Dice Psycho (29067)
        21. Doki Doki Blue Skies (28556)
        22. Chigau!!! (31573)
        23. Our Love (23046)
        24. Test Gaeshi (35695)
        25. Danganronpa V3: Killing Harmony (18334)
}
```

### Katawa Shoujo
```
Enter the VN_ID: 945
Recommendations for Katawa Shoujo:
Votes (1.0):
{
        1. Saya no Uta ~ The Song of Saya (97)
        2. Fate/stay night (11)
        3. The Fruit of Grisaia (5154)
        4. Steins;Gate (2002)
        5. G-senjou no Maou - The Devil on G-String (211)
        6. CLANNAD (4)
        7. Doki Doki Literature Club! (21905)
        8. Muv-Luv Alternative (92)
        9. Danganronpa: Trigger Happy Havoc (7014)
        10. Majikoi! Love Me Seriously!! (1143)
        11. Little Busters! (5)
        12. Umineko When They Cry - Question Arcs (24)
        13. Tsukihime (7)
        14. Muv-Luv (93)
        15. Ever17 -out of infinity- (17)
        16. Rewrite (751)
        17. Sharin no Kuni: The Girl Among the Sunflowers (57)
        18. Danganronpa 2: Goodbye Despair (7679)
        19. planetarian ~Dream of Little Star~ (34)
        20. Yume Miru Kusuri - A Drug That Makes You Dream (44)
        21. Umineko When They Cry - Answer Arcs (2153)
        22. Higurashi When They Cry - Question Arcs (67)
        23. Kara no Shojo (810)
        24. 999: Nine Hours, Nine Persons, Nine Doors (3112)
        25. Phoenix Wright: Ace Attorney (711)
}

Tags (1.5):
{
        1. ONE ~To the Radiant Season~ (51)
        2. Sakaagari Hurricane - Let's Pile Up Our School!! (1199)
        3. Soshite Ashita no Sekai yori (420)
        4. No One But You (17564)
        5. Season of the Sakura (206)
        6. Hatsukoi 1/1 (9124)
        7. Doki Doki Blue Skies (28556)
        8. Yume Miru Kusuri - A Drug That Makes You Dream (44)
        9. Passage! ~Passage of Life~ (15282)
        10. Homeward (7536)
        11. If My Heart Had Wings (9093)
        12. Daitoshokan no Hitsujikai -Dreaming Sheep- (12480)
        13. Princess Evangile (6710)
        14. D.S. -Dal Segno- (17742)
        15. Kanojo x Kanojo x Kanojo Dokidoki Full Throttle! (1442)
        16. Kono Aozora ni Yakusoku o (182)
        17. Tsuyokiss 2gakki (398)
        18. MeltyMoment (12830)
        19. Saku Saku: Love Blooms with the Cherry Blossoms (10304)
        20. Daitoshokan no Hitsujikai (8158)
        21. LOVELY×CATION2 (10288)
        22. Club Life (18708)
        23. Signal Heart Plus (3132)
        24. Period (573)
        25. Hime nochi Honey (814)
}

Combined:
{
        1. ONE ~To the Radiant Season~ (51)
        2. Sakaagari Hurricane - Let's Pile Up Our School!! (1199)
        3. Soshite Ashita no Sekai yori (420)
        4. Saya no Uta ~ The Song of Saya (97)
        5. No One But You (17564)
        6. Fate/stay night (11)
        7. Season of the Sakura (206)
        8. The Fruit of Grisaia (5154)
        9. Hatsukoi 1/1 (9124)
        10. Doki Doki Blue Skies (28556)
        11. Steins;Gate (2002)
        12. G-senjou no Maou - The Devil on G-String (211)
        13. Yume Miru Kusuri - A Drug That Makes You Dream (44)
        14. CLANNAD (4)
        15. Passage! ~Passage of Life~ (15282)
        16. Homeward (7536)
        17. If My Heart Had Wings (9093)
        18. Doki Doki Literature Club! (21905)
        19. Muv-Luv Alternative (92)
        20. Daitoshokan no Hitsujikai -Dreaming Sheep- (12480)
        21. Danganronpa: Trigger Happy Havoc (7014)
        22. Majikoi! Love Me Seriously!! (1143)
        23. Princess Evangile (6710)
        24. Little Busters! (5)
        25. D.S. -Dal Segno- (17742)
}
```

### Family Project
```
Enter the VN_ID: 155
Recommendations for Family Project ~Kazoku Keikaku~:
Votes (1.0):
{
        1. Fate/stay night (11)
        2. G-senjou no Maou - The Devil on G-String (211)
        3. Sharin no Kuni: The Girl Among the Sunflowers (57)
        4. Yume Miru Kusuri - A Drug That Makes You Dream (44)
        5. Ever17 -out of infinity- (17)
        6. CLANNAD (4)
        7. CROSS†CHANNEL (66)
        8. Saya no Uta ~ The Song of Saya (97)
        9. Tsukihime (7)
        10. Muv-Luv Alternative (92)
        11. The Fruit of Grisaia (5154)
        12. Majikoi! Love Me Seriously!! (1143)
        13. Katawa Shoujo (945)
        14. Kira Kira (414)
        15. Little Busters! (5)
        16. Muv-Luv (93)
        17. Utawarerumono (3)
        18. Steins;Gate (2002)
        19. Sengoku Rance (487)
        20. Hoshizora no Memoria -Wish upon a Shooting Star- (1474)
        21. Edelweiss (903)
        22. Rewrite (751)
        23. SHUFFLE! (28)
        24. Kara no Shojo (810)
        25. Snow Sakura (71)
}

Tags (1.5):
{
        1. Yoru Meguru, Bokura no Maigo Kyoushitsu (21405)
        2. Yoake Mae yori Ruri Iro na (232)
        3. Hermit Complex (3028)
        4. Haruka Kanata (13628)
        5. Itazurakko ~Uchi no Musume ni Kagitte~ (10660)
        6. Night Strangers (39677)
        7. Kud Wafter (3079)
        8. Soshite Ashita no Sekai yori (420)
        9. Yume Miru Kusuri - A Drug That Makes You Dream (44)
        10. Chibi Chibi Fiancee (2132)
        11. Canvas 2 ~Akaneiro no Palette~ (174)
        12. Seirei no Nemuru Mori - Forest Of Fate (30545)
        13. Eien no Owari ni (1207)
        14. Shin NOZOKI-ma ~Gesshukuya Kanshi 24 Ji~ (7025)
        15. Karigurashi Ren'ai (22045)
        16. Which girl should I choose? (898)
        17. ONE ~To the Radiant Season~ (51)
        18. Hatsukoi (750)
        19. My Little Kitties (17894)
        20. Reiki Ariel ~Prologue~ (35553)
        21. Shoujo Ryoujoku Juku (36032)
        22. WHITE ALBUM 2 ~closing chapter~ (7771)
        23. Kazoku Keikaku ~Soshite Mata Kazoku Keikaku o~ (3184)
        24. Karenai Sekai to Owaru Hana (19658)
        25. Cafe Sourire (4985)
}

Combined:
{
        1. Yoru Meguru, Bokura no Maigo Kyoushitsu (21405)
        2. Fate/stay night (11)
        3. Yume Miru Kusuri - A Drug That Makes You Dream (44)
        4. G-senjou no Maou - The Devil on G-String (211)
        5. Sharin no Kuni: The Girl Among the Sunflowers (57)
        6. Yoake Mae yori Ruri Iro na (232)
        7. Hermit Complex (3028)
        8. Haruka Kanata (13628)
        9. Ever17 -out of infinity- (17)
        10. CLANNAD (4)
        11. CROSS†CHANNEL (66)
        12. Itazurakko ~Uchi no Musume ni Kagitte~ (10660)
        13. Saya no Uta ~ The Song of Saya (97)
        14. Night Strangers (39677)
        15. Tsukihime (7)
        16. Kud Wafter (3079)
        17. Muv-Luv Alternative (92)
        18. The Fruit of Grisaia (5154)
        19. Majikoi! Love Me Seriously!! (1143)
        20. Soshite Ashita no Sekai yori (420)
        21. Katawa Shoujo (945)
        22. Kira Kira (414)
        23. Chibi Chibi Fiancee (2132)
        24. Little Busters! (5)
        25. Muv-Luv (93)
}
```

### Rance X - Showdown
```
Enter the VN_ID: 20802
Recommendations for Rance X - Showdown:
Votes (1.0):
{
        1. Sengoku Rance (487)
        2. Rance IX - The Helmanian Revolution (13802)
        3. Rance Quest (6985)
        4. Rance VI - Collapse of Zeth (2047)
        5. Rance 03 - The Fall of Leazas (17642)
        6. Steins;Gate (2002)
        7. Fate/stay night (11)
        8. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
        9. Muv-Luv Alternative (92)
        10. Saya no Uta ~ The Song of Saya (97)
        11. Full Metal Daemon Muramasa (2016)
        12. Rance 01 - Quest for Hikari (14022)
        13. G-senjou no Maou - The Devil on G-String (211)
        14. Umineko When They Cry - Question Arcs (24)
        15. BALDR SKY Dive2 "RECORDARE" (1913)
        16. BALDR SKY Dive1 "Lost Memory" (1306)
        17. The Fruit of Grisaia (5154)
        18. Ever17 -out of infinity- (17)
        19. Little Busters! (5)
        20. Rewrite (751)
        21. WHITE ALBUM 2 ~closing chapter~ (7771)
        22. Majikoi! Love Me Seriously!! (1143)
        23. Umineko When They Cry - Answer Arcs (2153)
        24. CLANNAD (4)
        25. Evenicle (16640)
}

Tags (1.5):
{
        1. DS Dengeki Bunko ADV: Baccano! (4698)
        2. Together - A Wish No One Remembers (27735)
        3. Magical Kanan (6261)
        4. Ore no Tsure wa Hito de Nashi (4868)
        5. Tomoyo After ~It's a Wonderful Life~ (12)
        6. Saint Estella Gakuin no Shichinin no Majo (12037)
        7. Missing Blue (1295)
        8. Love Esquire (24315)
        9. Rance IX - The Helmanian Revolution (13802)
        10. Trick and Treat (16549)
        11. Souda Love Revolution (17705)
        12. It Came From the Depths (6545)
        13. YU-NO - The Girl that Chants Love at the Edge of the World (1377)
        14. Love Letter (4948)
        15. √Letter (18644)
        16. Kingdom (110)
        17. CLANNAD (4)
        18. Soul Link (617)
        19. White Clarity (794)
        20. The God of Death (2352)
        21. Kiriya Hakushakuke no Roku Shimai (4040)
        22. Popotan (196)
        23. Kara no Shojo - The Second Episode (5922)
        24. Koi wa Sotto Saku Hana no You ni ~Futari wa Eien ni Yorisotte Iku~ (24782)
        25. Biniku no Kaori ~Netori Netorare Yari Yarare~ (470)
}

Combined:
{
        1. Rance IX - The Helmanian Revolution (13802)
        2. DS Dengeki Bunko ADV: Baccano! (4698)
        3. Together - A Wish No One Remembers (27735)
        4. Magical Kanan (6261)
        5. Ore no Tsure wa Hito de Nashi (4868)
        6. Sengoku Rance (487)
        7. Tomoyo After ~It's a Wonderful Life~ (12)
        8. Saint Estella Gakuin no Shichinin no Majo (12037)
        9. Missing Blue (1295)
        10. Love Esquire (24315)
        11. Trick and Treat (16549)
        12. Souda Love Revolution (17705)
        13. It Came From the Depths (6545)
        14. Rance Quest (6985)
        15. Rance VI - Collapse of Zeth (2047)
        16. Rance 03 - The Fall of Leazas (17642)
        17. Steins;Gate (2002)
        18. Fate/stay night (11)
        19. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
        20. Muv-Luv Alternative (92)
        21. YU-NO - The Girl that Chants Love at the Edge of the World (1377)
        22. Love Letter (4948)
        23. √Letter (18644)
        24. Saya no Uta ~ The Song of Saya (97)
        25. Full Metal Daemon Muramasa (2016)
}
```

### DEARDROPS
```
Enter the VN_ID: 2368
Recommendations for DEARDROPS:
Votes (1.0):
{
        1. G-senjou no Maou - The Devil on G-String (211)
        2. The Fruit of Grisaia (5154)
        3. Majikoi! Love Me Seriously!! (1143)
        4. Fate/stay night (11)
        5. Katawa Shoujo (945)
        6. Sharin no Kuni: The Girl Among the Sunflowers (57)
        7. Hoshizora no Memoria -Wish upon a Shooting Star- (1474)
        8. Kira Kira (414)
        9. Little Busters! (5)
        10. Muv-Luv Alternative (92)
        11. CLANNAD (4)
        12. Steins;Gate (2002)
        13. Rewrite (751)
        14. Maji de Watashi ni Koishinasai! S (6245)
        15. Saya no Uta ~ The Song of Saya (97)
        16. Kamidori Alchemy Meister (5652)
        17. Yume Miru Kusuri - A Drug That Makes You Dream (44)
        18. Muv-Luv (93)
        19. If My Heart Had Wings (9093)
        20. My Girlfriend is the President (2622)
        21. Ever17 -out of infinity- (17)
        22. Tsukihime (7)
        23. Kara no Shojo (810)
        24. Edelweiss (903)
        25. CROSS†CHANNEL (66)
}

Tags (1.5):
{
        1. KIRA☆KIRA CURTAIN CALL (2123)
        2. Isamashii Chibi no Iinazuke (634)
        3. Kira Kira (414)
        4. Quartett! (82)
        5. Yume ka Utsutsu ka Matryoshka (11081)
        6. No One But You (17564)
        7. Morobito Kozorite ~Joy to the World! The Lord Is Come~ (6474)
        8. Hoshi Ori Yume Mirai (14265)
        9. Seihou no Prismgear (12372)
        10. Hyakka Ryouran Elixir (12084)
        11. Concerto. (5352)
        12. Qie Ting Qin Yu - Grobda Remix (22161)
        13. Bra-Ban! (532)
        14. Izayoi no Fortuna (9913)
        15. Chanter ~Kimi no Uta ga Todoitara~ (1219)
        16. Ashita no Kimi to Au Tame ni (423)
        17. W. L. O. Sekai Ren'ai Kikou (1181)
        18. Kamigakari Cross Heart! (8437)
        19. Brad's Summer (9227)
        20. Hatsukoi 1/1 (9124)
        21. Himawari no Kyoukai to Nagai Natsuyasumi (10557)
        22. Karigurashi Ren'ai (22045)
        23. Soshite Ashita no Sekai yori (420)
        24. Otome ga Tsumugu Koi no Canvas (7794)
        25. Passage! ~Passage of Life~ (15282)
}

Combined:
{
        1. Kira Kira (414)
        2. KIRA☆KIRA CURTAIN CALL (2123)
        3. Isamashii Chibi no Iinazuke (634)
        4. Quartett! (82)
        5. G-senjou no Maou - The Devil on G-String (211)
        6. The Fruit of Grisaia (5154)
        7. Yume ka Utsutsu ka Matryoshka (11081)
        8. No One But You (17564)
        9. Majikoi! Love Me Seriously!! (1143)
        10. Fate/stay night (11)
        11. Morobito Kozorite ~Joy to the World! The Lord Is Come~ (6474)
        12. Katawa Shoujo (945)
        13. Hoshi Ori Yume Mirai (14265)
        14. Seihou no Prismgear (12372)
        15. Sharin no Kuni: The Girl Among the Sunflowers (57)
        16. Hoshizora no Memoria -Wish upon a Shooting Star- (1474)
        17. Little Busters! (5)
        18. Muv-Luv Alternative (92)
        19. CLANNAD (4)
        20. Hyakka Ryouran Elixir (12084)
        21. Steins;Gate (2002)
        22. Rewrite (751)
        23. Concerto. (5352)
        24. Maji de Watashi ni Koishinasai! S (6245)
        25. Qie Ting Qin Yu - Grobda Remix (22161)
}
```
