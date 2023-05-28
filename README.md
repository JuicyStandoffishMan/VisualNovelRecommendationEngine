# Visual Novel Recommendation Engine
A simple visual novel recommendation engine using VNDB data dumps.

# [VNLike.org - Live Web Version](https://vnlike.org/)
Note: The website currently only supports VN suggestions.

# Quickstart
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

# VN Recommendations
**Execute vn_test.py:**
```
python vn_test.py
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

# Character Recommendations
**Execute char_test.py:**
```
python char_test.py
```

You should see some loading messages, followed by a prompt to enter the Char ID.
```
Loading char vns
Loading traits
Building knn sparse matrix
Building kNN model
Loading titles

Enter the Char ID:
```

Char is the VNDB char id (**without** the leading c). For example, https://vndb.org/v22768 would be **22768**.

## Using VNDB Data Dumps
This repo stores the necessary dumps as of **May 26, 2023**, but you can always update them manually by visiting [VNDB's Data Dumps](https://vndb.org/d14). Make sure the votes file is renamed to `votes`. The other files can be pulled out of the `db` folder from the nearly-complete database download. Place them in the local `data` folder.

## MySQL Dump
There is also a script for dumping recommendations and converting the PostgreSQL files VNDB uses to a MySQL database using `db_convert.py`.

## API Usage
### VN Recommendations:
```python
from vnrec import vn

engine = vn()
vn_id = 7771

top_votes = engine.get_user_recommendations(vn_id)
top_tags = engine.get_tag_recommendations(vn_id)
top_combined = engine.get_combined_recommendations(vn_id)
```

### Character Recommendations:
```python
from crec import vnchar

engine = vnchar()
char_id = 22768

top_traits = engine.get_trait_recommendations_scores(cid)
```

Alternatively, there are `_score` suffixes to the above which return not just the IDs of the VNs, but also their normalized scores.

### Ignored tags
There are tags ignored in the tag scoring, and is currently not at all exhaustive. It just uses some presentation ones, like ADV and NVL. The same field (with different IDs) is supported for both VNs and characters.
```python
self.ignore_tags = [32, 2040, 2461, 1434, 1431, 43]
```

## How it works

### VNs
There are 2 scoring systems:
- **User votes:** Gives a "people also liked". It only looks at the public votes supplied by VNDB, as anonymous votes are not available, and applies `vote_exp` **pre-average**.
- **Similar tags:** Gives a "visual novel like" by using non-zero tag weights. The library will average out all of the tag votes **after** applying `tag-exp` to their weights (while keeping the sign).

A very basic combination scoring system using weighted summation (`vote_weight` and `tag_weight` is also available). `tag_weight` defaults to 1.5 because the vote score tends to dominate and just give the most popular VNs.

### Characters
This is much simpler and just uses common traits, which is whatever VNDB labels as a trait. This includes personality, appearance, role, engages in/subject of, and items.

# Credits and License
This repo is MIT. See [VNDB's data license](https://vndb.org/d17#4) as well.

Huge shoutout to ChatGPT for writing most of the code and answering all my questions along the way.

# Examples
<details>
        
<summary>VN Recommendations</summary>
        
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

### Kin'iro Loveriche
```
Enter the VN_ID: 21852
Recommendations for Kinkoi: Golden Loveriche:
Votes (1.0):
{
        1. Aokana -Four Rhythms Across the Blue- (12849)
        2. Sabbat of the Witch (16044)
        3. The Fruit of Grisaia (5154)
        4. RIDDLE JOKER (22230)
        5. Senren＊Banka (19073)
        6. Making * Lovers (21552)
        7. Majikoi! Love Me Seriously!! (1143)
        8. 9-nine-:Episode 2 (21668)
        9. G-senjou no Maou - The Devil on G-String (211)
        10. 9-nine-:Episode 1 (19829)
        11. Kinkoi: Golden Time (24717)
        12. 9-nine-:Episode 4 (26523)
        13. Café Stella and the Reapers' Butterflies (26414)
        14. 9-nine-:Episode 3 (23740)
        15. Summer Pockets (20424)
        16. Fate/stay night (11)
        17. Fureraba ~Friend to Lover~ (11856)
        18. If My Heart Had Wings (9093)
        19. Koikari - Love For Hire (25366)
        20. DRACU-RIOT! (8213)
        21. Rewrite (751)
        22. Steins;Gate (2002)
        23. Little Busters! (5)
        24. The Labyrinth of Grisaia (7723)
        25. Hoshi Ori Yume Mirai (14265)
}

Tags (1.5):
{
        1. Kinkoi: Golden Time (24717)
        2. AMBITIOUS MISSION (33036)
        3. My Klutzy Cupid (31002)
        4. Katei Kyouin ~Sensei no Ecchi na Gohoubi~ (32983)
        5. Kakenuke★Seishun Sparking! (28286)
        6. Floral Flowlove (18842)
        7. Princess Evangile (6710)
        8. Hanasaki Work Spring! (16070)
        9. A Sky Full of Stars (16560)
        10. Zutto Sukishite Takusan Sukishite (11712)
        11. Anata ni Koi Suru Ren'ai Recette (20315)
        12. Amairo * Islenauts (12167)
        13. Namepu! (21771)
        14. The Princess, the Stray Cat, and Matters of the Heart (18148)
        15. Magical Marriage Lunatics!! (12559)
        16. PRIMAL HEARTS 2 (17038)
        17. Koi Suru Kanojo no Bukiyou na Butai (15393)
        18. Walkure Romanze More&More (10983)
        19. Aonatsu Line (24702)
        20. 9-nine-:Episode 1 (19829)
        21. Sousaku Kanojo no Ren'ai Koushiki (31136)
        22. Koinoha -Koi no Share House- (29005)
        23. Anikano Minato to Houkago Netori Lesson ♪ (21986)
        24. Houkago Cinderella (28283)
        25. Uchikano: Living with my Girlfriend (22658)
}

Combined:
{
        1. Kinkoi: Golden Time (24717)
        2. Aokana -Four Rhythms Across the Blue- (12849)
        3. Sabbat of the Witch (16044)
        4. The Fruit of Grisaia (5154)
        5. RIDDLE JOKER (22230)
        6. Senren＊Banka (19073)
        7. AMBITIOUS MISSION (33036)
        8. Making * Lovers (21552)
        9. Majikoi! Love Me Seriously!! (1143)
        10. My Klutzy Cupid (31002)
        11. Katei Kyouin ~Sensei no Ecchi na Gohoubi~ (32983)
        12. Kakenuke★Seishun Sparking! (28286)
        13. Floral Flowlove (18842)
        14. Princess Evangile (6710)
        15. 9-nine-:Episode 1 (19829)
        16. 9-nine-:Episode 2 (21668)
        17. G-senjou no Maou - The Devil on G-String (211)
        18. 9-nine-:Episode 4 (26523)
        19. Hanasaki Work Spring! (16070)
        20. A Sky Full of Stars (16560)
        21. Café Stella and the Reapers' Butterflies (26414)
        22. 9-nine-:Episode 3 (23740)
        23. Summer Pockets (20424)
        24. Zutto Sukishite Takusan Sukishite (11712)
        25. Anata ni Koi Suru Ren'ai Recette (20315)
}
```

### Princess Evangile
```
Enter the VN_ID: 6710
Recommendations for Princess Evangile:
Votes (1.0):
{
        1. The Fruit of Grisaia (5154)
        2. Majikoi! Love Me Seriously!! (1143)
        3. G-senjou no Maou - The Devil on G-String (211)
        4. If My Heart Had Wings (9093)
        5. Hoshizora no Memoria -Wish upon a Shooting Star- (1474)
        6. Katawa Shoujo (945)
        7. Noble ☆ Works (4806)
        8. Fate/stay night (11)
        9. Maji de Watashi ni Koishinasai! S (6245)
        10. Sabbat of the Witch (16044)
        11. Princess Evangile W Happiness (8900)
        12. Aokana -Four Rhythms Across the Blue- (12849)
        13. DRACU-RIOT! (8213)
        14. ChronoClock (16208)
        15. Little Busters! (5)
        16. CLANNAD (4)
        17. Rewrite (751)
        18. Steins;Gate (2002)
        19. Fureraba ~Friend to Lover~ (11856)
        20. The Labyrinth of Grisaia (7723)
        21. Muv-Luv Alternative (92)
        22. Sharin no Kuni: The Girl Among the Sunflowers (57)
        23. NEKOPARA Vol. 1 (15538)
        24. WAGAMAMA HIGH SPEC (17823)
        25. Love, Elections, & Chocolate (4028)
}

Tags (1.5):
{
        1. Princess Evangile W Happiness (8900)
        2. Hoshi Ori Yume Mirai (14265)
        3. IxSHE Tell (21956)
        4. With Ribbon (5209)
        5. Amakano (15679)
        6. E School Life (24935)
        7. Hoshizora no Memoria -Wish upon a Shooting Star- (1474)
        8. Mashiro-iro Symphony (1552)
        9. Magical Marriage Lunatics!! (12559)
        10. Noble ☆ Works (4806)
        11. Love, Elections, & Chocolate (4028)
        12. Golden Marriage (14264)
        13. Honey Coming (180)
        14. Yuyukana -Under the Starlight- (6471)
        15. Under One Wing (17827)
        16. Natsu no Iro no Nostalgia (16069)
        17. W. L. O. Sekai Ren'ai Kikou (1181)
        18. If My Heart Had Wings (9093)
        19. DRACU-RIOT! (8213)
        20. Hatsukoi 1/1 (9124)
        21. A Sky Full of Stars (16560)
        22. Daitoshokan no Hitsujikai (8158)
        23. Tsujidou-san no Jun'ai Road (9879)
        24. Zannen na Ore-tachi no Seishun Jijou. (15485)
        25. Strawberry Nauts (7507)
}

Combined:
{
        1. Princess Evangile W Happiness (8900)
        2. Hoshi Ori Yume Mirai (14265)
        3. The Fruit of Grisaia (5154)
        4. Majikoi! Love Me Seriously!! (1143)
        5. Hoshizora no Memoria -Wish upon a Shooting Star- (1474)
        6. IxSHE Tell (21956)
        7. G-senjou no Maou - The Devil on G-String (211)
        8. Noble ☆ Works (4806)
        9. If My Heart Had Wings (9093)
        10. With Ribbon (5209)
        11. Katawa Shoujo (945)
        12. Amakano (15679)
        13. Fate/stay night (11)
        14. E School Life (24935)
        15. Maji de Watashi ni Koishinasai! S (6245)
        16. Mashiro-iro Symphony (1552)
        17. Magical Marriage Lunatics!! (12559)
        18. Sabbat of the Witch (16044)
        19. DRACU-RIOT! (8213)
        20. Love, Elections, & Chocolate (4028)
        21. Golden Marriage (14264)
        22. Honey Coming (180)
        23. Yuyukana -Under the Starlight- (6471)
        24. Under One Wing (17827)
        25. Aokana -Four Rhythms Across the Blue- (12849)
}
```

### The Warmth Between Us
```
Enter the VN_ID: 28461
Recommendations for The Warmth Between Us:
Votes (1.0):
{
        1. The House in Fata Morgana (12402)
        2. Katawa Shoujo (945)
        3. G-senjou no Maou - The Devil on G-String (211)
        4. narcissu (10)
        5. Doki Doki Literature Club! (21905)
        6. planetarian ~Dream of Little Star~ (34)
        7. Aokana -Four Rhythms Across the Blue- (12849)
        8. Raging Loop (21289)
        9. The Fruit of Grisaia (5154)
        10. Steins;Gate (2002)
        11. YOU and ME and HER: A Love Story (7738)
        12. Fate/stay night (11)
        13. Saya no Uta ~ The Song of Saya (97)
        14. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
        15. Ever17 -out of infinity- (17)
        16. If My Heart Had Wings (9093)
        17. Kara no Shojo (810)
        18. ATRI -My Dear Moments- (27448)
        19. Umineko When They Cry - Question Arcs (24)
        20. Muv-Luv Alternative (92)
        21. AI: THE SOMNIUM FILES (26532)
        22. 999: Nine Hours, Nine Persons, Nine Doors (3112)
        23. Higurashi When They Cry - Question Arcs (67)
        24. Umineko When They Cry - Answer Arcs (2153)
        25. eden* They were only two, on the planet. (1286)
}

Tags (1.5):
{
        1. Take Rena Home (2084)
        2. Junpaku no Machi, Haiyuki no Bokura. (21799)
        3. A Winter's Daydream (23726)
        4. EMMA The Story (23062)
        5. Shinkyoku Soukai Polyphonica - The Black (2196)
        6. Broken Hearted (6749)
        7. Winter With You (33803)
        8. Ripples (988)
        9. The Scaglietti (3313)
        10. Mir ejo glazami... (15934)
        11. Video Letter (34107)
        12. Kolderka (16908)
        13. Last Message ~Saraba Itoshiki Hito Yo.~ (6241)
        14. Santa-neun Gyobogeul Ibeul Su Bakke Eopseo (20729)
        15. Postcards: A Visit with Grandma (16163)
        16. Kusarihime ~jamais vu~ (28009)
        17. Plain Song -Christmas Special- (290)
        18. Katekyo's first date (44889)
        19. Goshujin-sama, Seira ni Yume Mitai na Icha Love Gohoushi Sasete Itadakemasu ka (37016)
        20. Amayo no Mayoi Neko (23051)
        21. Free Love (10292)
        22. White Christmas (8522)
        23. Shinkyoku Soukai Polyphonica (228)
        24. Big Dipper (25046)
        25. Amaoto to Jidou Ningyou (32193)
}

Combined:
{
        1. Take Rena Home (2084)
        2. Junpaku no Machi, Haiyuki no Bokura. (21799)
        3. The House in Fata Morgana (12402)
        4. Katawa Shoujo (945)
        5. G-senjou no Maou - The Devil on G-String (211)
        6. A Winter's Daydream (23726)
        7. EMMA The Story (23062)
        8. Shinkyoku Soukai Polyphonica - The Black (2196)
        9. narcissu (10)
        10. Broken Hearted (6749)
        11. Winter With You (33803)
        12. Ripples (988)
        13. Doki Doki Literature Club! (21905)
        14. planetarian ~Dream of Little Star~ (34)
        15. The Scaglietti (3313)
        16. Aokana -Four Rhythms Across the Blue- (12849)
        17. Raging Loop (21289)
        18. The Fruit of Grisaia (5154)
        19. Mir ejo glazami... (15934)
        20. Video Letter (34107)
        21. Steins;Gate (2002)
        22. YOU and ME and HER: A Love Story (7738)
        23. Kolderka (16908)
        24. Last Message ~Saraba Itoshiki Hito Yo.~ (6241)
        25. Santa-neun Gyobogeul Ibeul Su Bakke Eopseo (20729)
}
```

### The Language of Love
```
Enter the VN_ID: 25832
Recommendations for The Language of Love:
Votes (1.0):
{
        1. Katawa Shoujo (945)
        2. If My Heart Had Wings (9093)
        3. The Fruit of Grisaia (5154)
        4. Making * Lovers (21552)
        5. Doki Doki Literature Club! (21905)
        6. Fate/stay night (11)
        7. Aokana -Four Rhythms Across the Blue- (12849)
        8. Majikoi! Love Me Seriously!! (1143)
        9. Sabbat of the Witch (16044)
        10. G-senjou no Maou - The Devil on G-String (211)
        11. Steins;Gate (2002)
        12. Muv-Luv Alternative (92)
        13. ChronoClock (16208)
        14. YOU and ME and HER: A Love Story (7738)
        15. Hoshi Ori Yume Mirai (14265)
        16. Fureraba ~Friend to Lover~ (11856)
        17. Saya no Uta ~ The Song of Saya (97)
        18. NEKOPARA Vol. 1 (15538)
        19. Princess Evangile (6710)
        20. Muv-Luv (93)
        21. Senren＊Banka (19073)
        22. Danganronpa: Trigger Happy Havoc (7014)
        23. CLANNAD (4)
        24. Nanairo Reincarnation (15473)
        25. Hoshizora no Memoria -Wish upon a Shooting Star- (1474)
}

Tags (1.5):
{
        1. Katekyo's first date (44889)
        2. Bittersweet Harvest (42906)
        3. Amarantus (35856)
        4. Anta no Omocha (17261)
        5. Retrieving the Past: Series One (24145)
        6. Himegoto Unbalance - Kokoro to Karada no Ecchi na Kankei?! (5093)
        7. Miageta Sora ni Ochiteiku (394)
        8. Love in the Clouds Above Trinity (22663)
        9. Ligarued (8947)
        10. Indecent Wife Hana (33839)
        11. Free Love (10292)
        12. Tomodachi Kara Koibito e (28562)
        13. Exciting Games (29552)
        14. CAGE-FOOL- (13447)
        15. Tantei Jinguuji Saburou: Kiken na Futari (21361)
        16. Polarity (27504)
        17. Dream Ending (26210)
        18. The Scaglietti (3313)
        19. Ohinasama ~Shiawase wa Suigin no Aji~ (3399)
        20. Osananajimi no Iru Kurashi (30213)
        21. Beside ~Shiawase wa Katawara ni~ (5965)
        22. ValentaIN: Ore ga Valentine da!! (10061)
        23. OctoKuma (44182)
        24. Introvert (27971)
        25. Ryuu-Koku (7647)
}

Combined:
{
        1. Katekyo's first date (44889)
        2. Katawa Shoujo (945)
        3. Bittersweet Harvest (42906)
        4. Amarantus (35856)
        5. Anta no Omocha (17261)
        6. Retrieving the Past: Series One (24145)
        7. Himegoto Unbalance - Kokoro to Karada no Ecchi na Kankei?! (5093)
        8. If My Heart Had Wings (9093)
        9. The Fruit of Grisaia (5154)
        10. Miageta Sora ni Ochiteiku (394)
        11. Love in the Clouds Above Trinity (22663)
        12. Ligarued (8947)
        13. Free Love (10292)
        14. Indecent Wife Hana (33839)
        15. Making * Lovers (21552)
        16. Tomodachi Kara Koibito e (28562)
        17. Doki Doki Literature Club! (21905)
        18. Fate/stay night (11)
        19. Aokana -Four Rhythms Across the Blue- (12849)
        20. Majikoi! Love Me Seriously!! (1143)
        21. Sabbat of the Witch (16044)
        22. G-senjou no Maou - The Devil on G-String (211)
        23. Steins;Gate (2002)
        24. Exciting Games (29552)
        25. Muv-Luv Alternative (92)
}
```

### The Most Forbidden Love in the World
```
Enter the VN_ID: 415
Recommendations for The Most Forbidden Love in the World:
Votes (1.0):
{
        1. The Fruit of Grisaia (5154)
        2. G-senjou no Maou - The Devil on G-String (211)
        3. Majikoi! Love Me Seriously!! (1143)
        4. Fate/stay night (11)
        5. Aokana -Four Rhythms Across the Blue- (12849)
        6. Muv-Luv Alternative (92)
        7. Steins;Gate (2002)
        8. Making * Lovers (21552)
        9. Saya no Uta ~ The Song of Saya (97)
        10. Sabbat of the Witch (16044)
        11. Sharin no Kuni: The Girl Among the Sunflowers (57)
        12. Maji de Watashi ni Koishinasai! S (6245)
        13. If My Heart Had Wings (9093)
        14. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
        15. Kinkoi: Golden Loveriche (21852)
        16. Hoshizora no Memoria -Wish upon a Shooting Star- (1474)
        17. The Labyrinth of Grisaia (7723)
        18. WHITE ALBUM 2 ~closing chapter~ (7771)
        19. Muv-Luv (93)
        20. Nanairo Reincarnation (15473)
        21. CLANNAD (4)
        22. WHITE ALBUM 2 ~introductory chapter~ (2920)
        23. Katawa Shoujo (945)
        24. Rewrite (751)
        25. Little Busters! (5)
}

Tags (1.5):
{
        1. Mama Love (1456)
        2. Princess Bride (197)
        3. Free Love (10292)
        4. Sister☆Boy (14473)
        5. Life with Mary (22369)
        6. Bazooka Cafe (116)
        7. My Heart Grows Fonder (25656)
        8. Double Sensei Life (303)
        9. Cafe Sourire (4985)
        10. Valentine's Rush (17115)
        11. Like a Butler (1313)
        12. Otome to Fureau, Hitotsu Yane no Shita (33377)
        13. Days Before the Festival (41076)
        14. Jukuren Ganbou ~Himeta Omoi to Midara na Ai no Katachi~ (3218)
        15. Sucre ~Sweet and Charming Time for You~ (7230)
        16. Tsuma Shibori (887)
        17. Aikano ~Yukizora no Triangle~ (25380)
        18. Ryuu-Koku (7647)
        19. Triangle (26634)
        20. Matching Kekkon ~Appli de Mitsukeru Saikou no Hanayome~ (25922)
        21. Okiba ga Nai! (3098)
        22. The Flower Shop: Summer In Fairbrook (5608)
        23. Ame Koi (15426)
        24. Tomodachi Kara Koibito e (28562)
        25. Rondo Leaflet (574)
}

Combined:
{
        1. Mama Love (1456)
        2. Princess Bride (197)
        3. Free Love (10292)
        4. The Fruit of Grisaia (5154)
        5. G-senjou no Maou - The Devil on G-String (211)
        6. Majikoi! Love Me Seriously!! (1143)
        7. Sister☆Boy (14473)
        8. Life with Mary (22369)
        9. Fate/stay night (11)
        10. Aokana -Four Rhythms Across the Blue- (12849)
        11. Muv-Luv Alternative (92)
        12. Bazooka Cafe (116)
        13. My Heart Grows Fonder (25656)
        14. Double Sensei Life (303)
        15. Steins;Gate (2002)
        16. Cafe Sourire (4985)
        17. Valentine's Rush (17115)
        18. Like a Butler (1313)
        19. Otome to Fureau, Hitotsu Yane no Shita (33377)
        20. Days Before the Festival (41076)
        21. Jukuren Ganbou ~Himeta Omoi to Midara na Ai no Katachi~ (3218)
        22. Making * Lovers (21552)
        23. Saya no Uta ~ The Song of Saya (97)
        24. Sabbat of the Witch (16044)
        25. Sharin no Kuni: The Girl Among the Sunflowers (57)
}
```

### If My Heart Had Wings
```
Enter the VN_ID: 9093
Recommendations for If My Heart Had Wings:
Votes (1.0):
{
        1. The Fruit of Grisaia (5154)
        2. Katawa Shoujo (945)
        3. G-senjou no Maou - The Devil on G-String (211)
        4. Majikoi! Love Me Seriously!! (1143)
        5. Fate/stay night (11)
        6. Steins;Gate (2002)
        7. Hoshizora no Memoria -Wish upon a Shooting Star- (1474)
        8. CLANNAD (4)
        9. Little Busters! (5)
        10. Rewrite (751)
        11. Aokana -Four Rhythms Across the Blue- (12849)
        12. Saya no Uta ~ The Song of Saya (97)
        13. Muv-Luv Alternative (92)
        14. Maji de Watashi ni Koishinasai! S (6245)
        15. Sharin no Kuni: The Girl Among the Sunflowers (57)
        16. The Labyrinth of Grisaia (7723)
        17. Princess Evangile (6710)
        18. Sabbat of the Witch (16044)
        19. NEKOPARA Vol. 1 (15538)
        20. DRACU-RIOT! (8213)
        21. Muv-Luv (93)
        22. Noble ☆ Works (4806)
        23. Doki Doki Literature Club! (21905)
        24. Danganronpa: Trigger Happy Havoc (7014)
        25. The Eden of Grisaia (7724)
}

Tags (1.5):
{
        1. If My Heart Had Wings -Flight Diary- (10979)
        2. Under One Wing (17827)
        3. Daitoshokan no Hitsujikai (8158)
        4. Lovesick Puppies -Bokura wa Koi Suru Tame ni Umaretekita- (11194)
        5. Hoshizora no Memoria -Wish upon a Shooting Star- (1474)
        6. Princess Evangile (6710)
        7. Snow Sakura (71)
        8. Love, Elections, & Chocolate (4028)
        9. Majikoi! Love Me Seriously!! (1143)
        10. Suzukaze no Melt -Where wishes are drawn to each other- (3992)
        11. Hello, Goodbye (5316)
        12. If You Love Me, Then Say So! (17376)
        13. Hoshi Ori Yume Mirai (14265)
        14. Maji de Watashi ni Koishinasai! S (6245)
        15. Strawberry Nauts (7507)
        16. Sorairo Innocent (17980)
        17. SHUFFLE! (28)
        18. A Sky Full of Stars (16560)
        19. Hoshiuta (1002)
        20. Saku Saku: Love Blooms with the Cherry Blossoms (10304)
        21. Amakano (15679)
        22. Aonatsu Line (24702)
        23. Hatsukoi 1/1 (9124)
        24. Aokana -Four Rhythms Across the Blue- (12849)
        25. Edelweiss (903)
}

Combined:
{
        1. If My Heart Had Wings -Flight Diary- (10979)
        2. The Fruit of Grisaia (5154)
        3. Under One Wing (17827)
        4. Hoshizora no Memoria -Wish upon a Shooting Star- (1474)
        5. Majikoi! Love Me Seriously!! (1143)
        6. Daitoshokan no Hitsujikai (8158)
        7. Katawa Shoujo (945)
        8. G-senjou no Maou - The Devil on G-String (211)
        9. Princess Evangile (6710)
        10. Lovesick Puppies -Bokura wa Koi Suru Tame ni Umaretekita- (11194)
        11. Fate/stay night (11)
        12. Snow Sakura (71)
        13. Steins;Gate (2002)
        14. CLANNAD (4)
        15. Love, Elections, & Chocolate (4028)
        16. Little Busters! (5)
        17. Rewrite (751)
        18. Maji de Watashi ni Koishinasai! S (6245)
        19. Aokana -Four Rhythms Across the Blue- (12849)
        20. Suzukaze no Melt -Where wishes are drawn to each other- (3992)
        21. Saya no Uta ~ The Song of Saya (97)
        22. Muv-Luv Alternative (92)
        23. Hello, Goodbye (5316)
        24. Sharin no Kuni: The Girl Among the Sunflowers (57)
        25. If You Love Me, Then Say So! (17376)
}
```

### Ever17
```
Enter the VN_ID: 17
Recommendations for Ever17 -out of infinity-:
Votes (1.0):
{
        1. Fate/stay night (11)
        2. Saya no Uta ~ The Song of Saya (97)
        3. Steins;Gate (2002)
        4. G-senjou no Maou - The Devil on G-String (211)
        5. Umineko When They Cry - Question Arcs (24)
        6. Muv-Luv Alternative (92)
        7. CLANNAD (4)
        8. Sharin no Kuni: The Girl Among the Sunflowers (57)
        9. Tsukihime (7)
        10. Umineko When They Cry - Answer Arcs (2153)
        11. Katawa Shoujo (945)
        12. Little Busters! (5)
        13. 999: Nine Hours, Nine Persons, Nine Doors (3112)
        14. Rewrite (751)
        15. planetarian ~Dream of Little Star~ (34)
        16. Danganronpa: Trigger Happy Havoc (7014)
        17. Muv-Luv (93)
        18. The Fruit of Grisaia (5154)
        19. Remember11 -the age of infinity- (13)
        20. Higurashi When They Cry - Question Arcs (67)
        21. Danganronpa 2: Goodbye Despair (7679)
        22. Kara no Shojo (810)
        23. Phoenix Wright: Ace Attorney (711)
        24. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
        25. CROSS†CHANNEL (66)
}

Tags (1.5):
{
        1. Ever17 (19373)
        2. Root Double -Before Crime * After Days- (5000)
        3. 12RIVEN -the Ψcliminal of integral- (247)
        4. Remember11 -the age of infinity- (13)
        5. Tsukiakari Lunch (10999)
        6. Never7 -the end of infinity- (248)
        7. Zero Escape: Virtue's Last Reward (7809)
        8. Trick and Treat (16549)
        9. I/O (96)
        10. 999: Nine Hours, Nine Persons, Nine Doors (3112)
        11. Daylight -Asa ni Hikari no Kan o- (1614)
        12. Diorama (5372)
        13. Date A Live: Arusu Install (14706)
        14. Soul Link (617)
        15. Beyond R: Rule Ripper (39825)
        16. Dei Gratia no Rashinban (16435)
        17. Amnesia: Memories (7803)
        18. Symphonic Rain (38)
        19. Endless Jade Sea -Midori no Umi- (7238)
        20. ENIGMA: (18315)
        21. Himawari - The Sunflower - (210)
        22. Akaya Akashiya Ayakashino (5841)
        23. ISLAND (18498)
        24. Norn9: Var Commons (11179)
        25. Head AS Code (29960)
}

Combined:
{
        1. Ever17 (19373)
        2. Fate/stay night (11)
        3. Saya no Uta ~ The Song of Saya (97)
        4. Steins;Gate (2002)
        5. G-senjou no Maou - The Devil on G-String (211)
        6. Umineko When They Cry - Question Arcs (24)
        7. Muv-Luv Alternative (92)
        8. 999: Nine Hours, Nine Persons, Nine Doors (3112)
        9. Remember11 -the age of infinity- (13)
        10. CLANNAD (4)
        11. Root Double -Before Crime * After Days- (5000)
        12. Sharin no Kuni: The Girl Among the Sunflowers (57)
        13. Tsukihime (7)
        14. 12RIVEN -the Ψcliminal of integral- (247)
        15. Umineko When They Cry - Answer Arcs (2153)
        16. Katawa Shoujo (945)
        17. Little Busters! (5)
        18. Tsukiakari Lunch (10999)
        19. Never7 -the end of infinity- (248)
        20. Zero Escape: Virtue's Last Reward (7809)
        21. Rewrite (751)
        22. Trick and Treat (16549)
        23. I/O (96)
        24. planetarian ~Dream of Little Star~ (34)
        25. Danganronpa: Trigger Happy Havoc (7014)
}
```

### Ace Attorney
```
Enter the VN_ID: 711
Recommendations for Phoenix Wright: Ace Attorney:
Votes (1.0):
{
        1. Phoenix Wright: Ace Attorney - Trials and Tribulations (716)
        2. Phoenix Wright: Ace Attorney - Justice for All (715)
        3. Danganronpa: Trigger Happy Havoc (7014)
        4. 999: Nine Hours, Nine Persons, Nine Doors (3112)
        5. Danganronpa 2: Goodbye Despair (7679)
        6. Steins;Gate (2002)
        7. Umineko When They Cry - Question Arcs (24)
        8. Fate/stay night (11)
        9. Saya no Uta ~ The Song of Saya (97)
        10. Apollo Justice: Ace Attorney (717)
        11. Umineko When They Cry - Answer Arcs (2153)
        12. Zero Escape: Virtue's Last Reward (7809)
        13. Danganronpa V3: Killing Harmony (18334)
        14. Higurashi When They Cry - Question Arcs (67)
        15. Katawa Shoujo (945)
        16. Ever17 -out of infinity- (17)
        17. Doki Doki Literature Club! (21905)
        18. Muv-Luv Alternative (92)
        19. G-senjou no Maou - The Devil on G-String (211)
        20. Tsukihime (7)
        21. Ace Attorney Investigations: Miles Edgeworth (1719)
        22. Higurashi When They Cry - Answer Arcs (68)
        23. Phoenix Wright: Ace Attorney - Dual Destinies (9889)
        24. CLANNAD (4)
        25. Muv-Luv (93)
}

Tags (1.5):
{
        1. Phoenix Wright: Ace Attorney - Justice for All (715)
        2. Phoenix Wright: Ace Attorney - Trials and Tribulations (716)
        3. Apollo Justice: Ace Attorney (717)
        4. Phoenix Wright: Ace Attorney - Dual Destinies (9889)
        5. Ace Attorney Investigations: Miles Edgeworth: Prosecutor's Path (6639)
        6. Ace Attorney Investigations: Miles Edgeworth (1719)
        7. Phoenix Wright: Ace Attorney - Spirit of Justice (18267)
        8. Apollo Justice Case 5 : Turnabout Substitution (5632)
        9. The Great Ace Attorney: Adventures (15125)
        10. The Great Ace Attorney 2: Resolve (19987)
        11. of the Devil (37866)
        12. Turnabout Revolution (17893)
        13. Phoenix Wright: Ace Attorney - The Contempt of Court (5633)
        14. Phoenix Wright: Ace Attorney - Conflict of Interest (13735)
        15. Professor Layton vs. Phoenix Wright: Ace Attorney (15119)
        16. Aviary Attorney (18850)
        17. Last Window: The Secret of Cape West (4617)
        18. Jake Hunter Detective Story: Memories of the Past (1574)
        19. Hotel Dusk: Room 215 (697)
        20. Turnabout of Courage (12515)
        21. Phoenix Wright: World Of Justice (9991)
        22. Kansei (7594)
        23. Again (4080)
        24. Occult Crime Police (24884)
        25. Attorney D (9263)
}

Combined:
{
        1. Phoenix Wright: Ace Attorney - Trials and Tribulations (716)
        2. Phoenix Wright: Ace Attorney - Justice for All (715)
        3. Apollo Justice: Ace Attorney (717)
        4. Phoenix Wright: Ace Attorney - Dual Destinies (9889)
        5. Ace Attorney Investigations: Miles Edgeworth: Prosecutor's Path (6639)
        6. Ace Attorney Investigations: Miles Edgeworth (1719)
        7. Phoenix Wright: Ace Attorney - Spirit of Justice (18267)
        8. Apollo Justice Case 5 : Turnabout Substitution (5632)
        9. The Great Ace Attorney: Adventures (15125)
        10. The Great Ace Attorney 2: Resolve (19987)
        11. Danganronpa: Trigger Happy Havoc (7014)
        12. of the Devil (37866)
        13. 999: Nine Hours, Nine Persons, Nine Doors (3112)
        14. Turnabout Revolution (17893)
        15. Phoenix Wright: Ace Attorney - The Contempt of Court (5633)
        16. Danganronpa 2: Goodbye Despair (7679)
        17. Phoenix Wright: Ace Attorney - Conflict of Interest (13735)
        18. Steins;Gate (2002)
        19. Umineko When They Cry - Question Arcs (24)
        20. Professor Layton vs. Phoenix Wright: Ace Attorney (15119)
        21. Aviary Attorney (18850)
        22. Fate/stay night (11)
        23. Saya no Uta ~ The Song of Saya (97)
        24. Last Window: The Secret of Cape West (4617)
        25. Umineko When They Cry - Answer Arcs (2153)
}
```

### Little Busters!
```
Enter the VN_ID: 5
Recommendations for Little Busters!:
Votes (1.0):
{
        1. CLANNAD (4)
        2. Rewrite (751)
        3. Fate/stay night (11)
        4. G-senjou no Maou - The Devil on G-String (211)
        5. Steins;Gate (2002)
        6. The Fruit of Grisaia (5154)
        7. Muv-Luv Alternative (92)
        8. Saya no Uta ~ The Song of Saya (97)
        9. Katawa Shoujo (945)
        10. Majikoi! Love Me Seriously!! (1143)
        11. Sharin no Kuni: The Girl Among the Sunflowers (57)
        12. Umineko When They Cry - Question Arcs (24)
        13. Ever17 -out of infinity- (17)
        14. planetarian ~Dream of Little Star~ (34)
        15. Muv-Luv (93)
        16. Tsukihime (7)
        17. Umineko When They Cry - Answer Arcs (2153)
        18. Danganronpa: Trigger Happy Havoc (7014)
        19. Hoshizora no Memoria -Wish upon a Shooting Star- (1474)
        20. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
        21. Danganronpa 2: Goodbye Despair (7679)
        22. Higurashi When They Cry - Question Arcs (67)
        23. Kanon (33)
        24. CROSS†CHANNEL (66)
        25. Kara no Shojo (810)
}

Tags (1.5):
{
        1. CLANNAD (4)
        2. Majikoi! Love Me Seriously!! (1143)
        3. Rewrite (751)
        4. Hoshizora no Memoria -Wish upon a Shooting Star- (1474)
        5. Daitoshokan no Hitsujikai (8158)
        6. Maji de Watashi ni Koishinasai! S (6245)
        7. ONE ~To the Radiant Season~ (51)
        8. Flyable Heart (1179)
        9. Endless Jade Sea -Midori no Umi- (7238)
        10. Ore-tachi ni Tsubasa wa Nai ―――under the innocent sky. (1141)
        11. AstralAir no Shiroki Towa (12984)
        12. The logic of the miniature garden (14924)
        13. Love, Elections, & Chocolate (4028)
        14. Wind -a breath of heart- (35)
        15. Summer Pockets (20424)
        16. Muv-Luv (93)
        17. MeltyMoment (12830)
        18. Amatarasu Riddle Star (12992)
        19. 11eyes -Tsumi to Batsu to Aganai no Shoujo- (729)
        20. D.S. -Dal Segno- (17742)
        21. AIR (36)
        22. Omoide Kakaete Ai ni Koi!! (31125)
        23. To Heart (18)
        24. If My Heart Had Wings (9093)
        25. Ayakashibito (646)
}

Combined:
{
        1. CLANNAD (4)
        2. Rewrite (751)
        3. Majikoi! Love Me Seriously!! (1143)
        4. Hoshizora no Memoria -Wish upon a Shooting Star- (1474)
        5. Fate/stay night (11)
        6. G-senjou no Maou - The Devil on G-String (211)
        7. Daitoshokan no Hitsujikai (8158)
        8. Maji de Watashi ni Koishinasai! S (6245)
        9. Steins;Gate (2002)
        10. The Fruit of Grisaia (5154)
        11. ONE ~To the Radiant Season~ (51)
        12. Muv-Luv Alternative (92)
        13. Flyable Heart (1179)
        14. Saya no Uta ~ The Song of Saya (97)
        15. Endless Jade Sea -Midori no Umi- (7238)
        16. Muv-Luv (93)
        17. Katawa Shoujo (945)
        18. Sharin no Kuni: The Girl Among the Sunflowers (57)
        19. Umineko When They Cry - Question Arcs (24)
        20. Ore-tachi ni Tsubasa wa Nai ―――under the innocent sky. (1141)
        21. Ever17 -out of infinity- (17)
        22. planetarian ~Dream of Little Star~ (34)
        23. AstralAir no Shiroki Towa (12984)
        24. The logic of the miniature garden (14924)
        25. Love, Elections, & Chocolate (4028)
}
```

### Riddle Joker
```
Enter the VN_ID: 22230
Recommendations for RIDDLE JOKER:
Votes (1.0):
{
        1. Sabbat of the Witch (16044)
        2. Senren＊Banka (19073)
        3. Aokana -Four Rhythms Across the Blue- (12849)
        4. Kinkoi: Golden Loveriche (21852)
        5. The Fruit of Grisaia (5154)
        6. Making * Lovers (21552)
        7. Café Stella and the Reapers' Butterflies (26414)
        8. Majikoi! Love Me Seriously!! (1143)
        9. 9-nine-:Episode 2 (21668)
        10. 9-nine-:Episode 1 (19829)
        11. DRACU-RIOT! (8213)
        12. 9-nine-:Episode 4 (26523)
        13. G-senjou no Maou - The Devil on G-String (211)
        14. 9-nine-:Episode 3 (23740)
        15. Fureraba ~Friend to Lover~ (11856)
        16. If My Heart Had Wings (9093)
        17. Summer Pockets (20424)
        18. Noble ☆ Works (4806)
        19. Koikari - Love For Hire (25366)
        20. ChronoClock (16208)
        21. Fate/stay night (11)
        22. WAGAMAMA HIGH SPEC (17823)
        23. Hoshi Ori Yume Mirai (14265)
        24. Sankaku Ren'ai: Love Triangle Trouble (19444)
        25. The Labyrinth of Grisaia (7723)
}

Tags (1.5):
{
        1. Sabbat of the Witch (16044)
        2. Senren＊Banka (19073)
        3. Hello, Goodbye (5316)
        4. DRACU-RIOT! (8213)
        5. WAGAMAMA HIGH SPEC (17823)
        6. Clover Day's (13325)
        7. Princess Evangile (6710)
        8. Imouto no Katachi (6291)
        9. SuGirly Wish (7068)
        10. Hello Lady! (13631)
        11. PRIMAL HEARTS 2 (17038)
        12. Ninki Seiyuu: How to Make a Pop Voice Actress (20148)
        13. Deatte 5-fun wa Ore no Mono! Jikan Teishi to Atropos (23388)
        14. PRIMAL HEARTS (14887)
        15. Hime nochi Honey (814)
        16. Wind -a breath of heart- (35)
        17. A Sky Full of Stars (16560)
        18. Lover Able (5734)
        19. Harvest OverRay (14761)
        20. Kakenuke★Seishun Sparking! (28286)
        21. Amakano 2 (26307)
        22. ALIA's CARNIVAL! (11301)
        23. Ichiban Janakya Dame Desu ka? (12479)
        24. Hoshi Ori Yume Mirai (14265)
        25. IxSHE Tell (21956)
}

Combined:
{
        1. Sabbat of the Witch (16044)
        2. Senren＊Banka (19073)
        3. Hello, Goodbye (5316)
        4. DRACU-RIOT! (8213)
        5. Aokana -Four Rhythms Across the Blue- (12849)
        6. WAGAMAMA HIGH SPEC (17823)
        7. Clover Day's (13325)
        8. Kinkoi: Golden Loveriche (21852)
        9. Princess Evangile (6710)
        10. The Fruit of Grisaia (5154)
        11. Making * Lovers (21552)
        12. Imouto no Katachi (6291)
        13. Café Stella and the Reapers' Butterflies (26414)
        14. SuGirly Wish (7068)
        15. Hello Lady! (13631)
        16. Majikoi! Love Me Seriously!! (1143)
        17. PRIMAL HEARTS 2 (17038)
        18. 9-nine-:Episode 2 (21668)
        19. 9-nine-:Episode 1 (19829)
        20. Ninki Seiyuu: How to Make a Pop Voice Actress (20148)
        21. 9-nine-:Episode 4 (26523)
        22. G-senjou no Maou - The Devil on G-String (211)
        23. Deatte 5-fun wa Ore no Mono! Jikan Teishi to Atropos (23388)
        24. 9-nine-:Episode 3 (23740)
        25. Fureraba ~Friend to Lover~ (11856)
}
```

### 9-nine-:Episode 1
```
Enter the VN_ID: 19829
Recommendations for 9-nine-:Episode 1:
Votes (1.0):
{
        1. 9-nine-:Episode 2 (21668)
        2. 9-nine-:Episode 3 (23740)
        3. 9-nine-:Episode 4 (26523)
        4. Aokana -Four Rhythms Across the Blue- (12849)
        5. The Fruit of Grisaia (5154)
        6. Sabbat of the Witch (16044)
        7. Senren＊Banka (19073)
        8. RIDDLE JOKER (22230)
        9. Kinkoi: Golden Loveriche (21852)
        10. G-senjou no Maou - The Devil on G-String (211)
        11. Summer Pockets (20424)
        12. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
        13. Saya no Uta ~ The Song of Saya (97)
        14. Fate/stay night (11)
        15. Steins;Gate (2002)
        16. Majikoi! Love Me Seriously!! (1143)
        17. Rewrite (751)
        18. Muv-Luv Alternative (92)
        19. Making * Lovers (21552)
        20. Little Busters! (5)
        21. 9-nine-:NewEpisode (29724)
        22. The Labyrinth of Grisaia (7723)
        23. Umineko When They Cry - Question Arcs (24)
        24. CLANNAD (4)
        25. If My Heart Had Wings (9093)
}

Tags (1.5):
{
        1. 9-nine-:Episode 2 (21668)
        2. 9-nine-:Episode 3 (23740)
        3. 9-nine-:Episode 4 (26523)
        4. Aikagi 3 (30214)
        5. Keiken Zero na Classmate π (31471)
        6. Kiss Kara Hajimaru Gyaru no Koi ~Kurumi no Uwasa to Honto no Kimochi~ (32308)
        7. Boku to Kanojo no Gohoushi Dousei (23392)
        8. Little Sick Girls ~Osananajimi no Koibito~ (26183)
        9. Koushinchou Shoujo ~XL na Kanojo wa H na Nayami de Ippai! (16758)
        10. Yukigatari (2629)
        11. My Sweet Home (20000)
        12. Koi x Mitsu ~Yaeneri Saki to Akai Ito no Ouji-sama~ (30232)
        13. Kinkoi: Golden Loveriche (21852)
        14. Quickie: Toshiko (22558)
        15. Icha Love Dousei Seikatsu -Osananajimi to Asa kara Ban made Icha Icha Icha Icha- (21302)
        16. Quickie: Victoria (28774)
        17. Deep Love Diary -Koibito Nikki- (19719)
        18. Kanojo, Amai Kanojo (18253)
        19. Ayame no Machi to Ohime-sama (12974)
        20. Anikano Minato to Houkago Netori Lesson ♪ (21986)
        21. Amakano (15679)
        22. Katei Kyouin ~Sensei no Ecchi na Gohoubi~ (32983)
        23. Yami to Hikari no Sanctuary (21073)
        24. Koi wa Sotto Saku Hana no You ni (22561)
        25. Tsukikage no Simulacre (19964)
}

Combined:
{
        1. 9-nine-:Episode 2 (21668)
        2. 9-nine-:Episode 3 (23740)
        3. 9-nine-:Episode 4 (26523)
        4. Aokana -Four Rhythms Across the Blue- (12849)
        5. Aikagi 3 (30214)
        6. The Fruit of Grisaia (5154)
        7. Sabbat of the Witch (16044)
        8. Keiken Zero na Classmate π (31471)
        9. Kiss Kara Hajimaru Gyaru no Koi ~Kurumi no Uwasa to Honto no Kimochi~ (32308)
        10. Boku to Kanojo no Gohoushi Dousei (23392)
        11. Kinkoi: Golden Loveriche (21852)
        12. Senren＊Banka (19073)
        13. RIDDLE JOKER (22230)
        14. G-senjou no Maou - The Devil on G-String (211)
        15. Summer Pockets (20424)
        16. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
        17. Little Sick Girls ~Osananajimi no Koibito~ (26183)
        18. Saya no Uta ~ The Song of Saya (97)
        19. Koushinchou Shoujo ~XL na Kanojo wa H na Nayami de Ippai! (16758)
        20. Fate/stay night (11)
        21. Steins;Gate (2002)
        22. Majikoi! Love Me Seriously!! (1143)
        23. Rewrite (751)
        24. Muv-Luv Alternative (92)
        25. Yukigatari (2629)
}
```

### Planetarian
```
Enter the VN_ID: 34
Recommendations for planetarian ~Dream of Little Star~:
Votes (1.0):
{
        1. Saya no Uta ~ The Song of Saya (97)
        2. Fate/stay night (11)
        3. Steins;Gate (2002)
        4. CLANNAD (4)
        5. Little Busters! (5)
        6. G-senjou no Maou - The Devil on G-String (211)
        7. Ever17 -out of infinity- (17)
        8. Muv-Luv Alternative (92)
        9. Katawa Shoujo (945)
        10. Umineko When They Cry - Question Arcs (24)
        11. Rewrite (751)
        12. Tsukihime (7)
        13. The Fruit of Grisaia (5154)
        14. narcissu (10)
        15. Danganronpa: Trigger Happy Havoc (7014)
        16. Umineko When They Cry - Answer Arcs (2153)
        17. Muv-Luv (93)
        18. Sharin no Kuni: The Girl Among the Sunflowers (57)
        19. Higurashi When They Cry - Question Arcs (67)
        20. Wonderful Everyday ~Diskontinuierliches Dasein~ (3144)
        21. Doki Doki Literature Club! (21905)
        22. Danganronpa 2: Goodbye Despair (7679)
        23. 999: Nine Hours, Nine Persons, Nine Doors (3112)
        24. Phoenix Wright: Ace Attorney (711)
        25. Higurashi When They Cry - Answer Arcs (68)
}

Tags (1.5):
{
        1. Hoshi no Hito ~Planetarian Side Story~ (11921)
        2. Harmonia (16510)
        3. Issho ni Ikimashou Ikimashou Ikimashou (18915)
        4. To You of the Future, I Give Every Song (1560)
        5. Moonshine (1296)
        6. Kolderka (16908)
        7. EMMA The Story (23062)
        8. Shinkyoku Soukai Polyphonica ~Farewell Song~ (7727)
        9. Shinkyoku Soukai Polyphonica (228)
        10. From the Bottom of the Heart (1290)
        11. Take Rena Home (2084)
        12. Mirai no Uta to, Tsunagaru Hitomi (5481)
        13. Palinurus (17129)
        14. Junpaku no Machi, Haiyuki no Bokura. (21799)
        15. Subete ga Uso ni Naru (5455)
        16. Shinkyoku Soukai Polyphonica - The Black (2196)
        17. Until We Meet Again (230)
        18. The Meadow (12317)
        19. Broken Hearted (6749)
        20. Rewrite: Cradles Tale (21644)
        21. Natsuki Forever (22949)
        22. The Burial of our Dreams (37366)
        23. Watashi wa Onigiri (4023)
        24. 40 Days and 40 Nights of Rain (39)
        25. Midnight Chaos (14902)
}

Combined:
{
        1. Hoshi no Hito ~Planetarian Side Story~ (11921)
        2. Saya no Uta ~ The Song of Saya (97)
        3. Harmonia (16510)
        4. Issho ni Ikimashou Ikimashou Ikimashou (18915)
        5. Fate/stay night (11)
        6. To You of the Future, I Give Every Song (1560)
        7. Moonshine (1296)
        8. Steins;Gate (2002)
        9. CLANNAD (4)
        10. Kolderka (16908)
        11. Little Busters! (5)
        12. G-senjou no Maou - The Devil on G-String (211)
        13. Ever17 -out of infinity- (17)
        14. Muv-Luv Alternative (92)
        15. EMMA The Story (23062)
        16. Shinkyoku Soukai Polyphonica ~Farewell Song~ (7727)
        17. Shinkyoku Soukai Polyphonica (228)
        18. Katawa Shoujo (945)
        19. From the Bottom of the Heart (1290)
        20. Umineko When They Cry - Question Arcs (24)
        21. Take Rena Home (2084)
        22. Mirai no Uta to, Tsunagaru Hitomi (5481)
        23. Rewrite (751)
        24. Palinurus (17129)
        25. Tsukihime (7)
}
```

### Making * Lovers
```
Enter the VN_ID: 21552
Recommendations for Making * Lovers:
Votes (1.0):
{
        1. Aokana -Four Rhythms Across the Blue- (12849)
        2. Sabbat of the Witch (16044)
        3. The Fruit of Grisaia (5154)
        4. Senren＊Banka (19073)
        5. RIDDLE JOKER (22230)
        6. Fureraba ~Friend to Lover~ (11856)
        7. Majikoi! Love Me Seriously!! (1143)
        8. Kinkoi: Golden Loveriche (21852)
        9. If My Heart Had Wings (9093)
        10. G-senjou no Maou - The Devil on G-String (211)
        11. Hoshi Ori Yume Mirai (14265)
        12. Katawa Shoujo (945)
        13. Sugar * Style (24320)
        14. Sankaku Ren'ai: Love Triangle Trouble (19444)
        15. DRACU-RIOT! (8213)
        16. Fate/stay night (11)
        17. ChronoClock (16208)
        18. Noble ☆ Works (4806)
        19. Steins;Gate (2002)
        20. WAGAMAMA HIGH SPEC (17823)
        21. 9-nine-:Episode 2 (21668)
        22. Café Stella and the Reapers' Butterflies (26414)
        23. Koikari - Love For Hire (25366)
        24. Princess Evangile (6710)
        25. Maji de Watashi ni Koishinasai! S (6245)
}

Tags (1.5):
{
        1. Making*Lovers After Stories (22594)
        2. Lover Able (5734)
        3. Love Sweets (14269)
        4. Fureraba ~Friend to Lover~ (11856)
        5. Sankaku Ren'ai: Love Triangle Trouble (19444)
        6. Pure x Connect (16166)
        7. 1/1 Kareshi Kanojo (32655)
        8. Dousei Lover Able (7774)
        9. Zutto Sukishite Takusan Sukishite (11712)
        10. Haji Kano ~Kimi ga Iru Heya~ (27070)
        11. Deatte 5-fun wa Ore no Mono! Jikan Teishi to Atropos (23388)
        12. My Klutzy Cupid (31002)
        13. Amakano 2 (26307)
        14. Berry's (10933)
        15. Chihiro Himukai Always Walks Away (30118)
        16. Areas ~Sora ni Utsusu Kimi to no Sekai~ (1379)
        17. Majipuri -Wonder Cradle- (187)
        18. Koi x Koi = Infinity ~Koisuru Otome ni Dekiru Koto~ (12377)
        19. Sugar * Style (24320)
        20. Imouto Paradise 3 (21766)
        21. Fluorite Memories ~Itsuka Kitto, Yakusoku no Basho de~ (6652)
        22. Desperate Virgin Brother & Rebellious Little Sister (30458)
        23. Scramble Lovers (14595)
        24. LOVELY QUEST (10341)
        25. Suite Life (21706)
}

Combined:
{
        1. Making*Lovers After Stories (22594)
        2. Fureraba ~Friend to Lover~ (11856)
        3. Aokana -Four Rhythms Across the Blue- (12849)
        4. Sabbat of the Witch (16044)
        5. Lover Able (5734)
        6. The Fruit of Grisaia (5154)
        7. Senren＊Banka (19073)
        8. RIDDLE JOKER (22230)
        9. Love Sweets (14269)
        10. Majikoi! Love Me Seriously!! (1143)
        11. Kinkoi: Golden Loveriche (21852)
        12. Sankaku Ren'ai: Love Triangle Trouble (19444)
        13. If My Heart Had Wings (9093)
        14. G-senjou no Maou - The Devil on G-String (211)
        15. Pure x Connect (16166)
        16. Hoshi Ori Yume Mirai (14265)
        17. 1/1 Kareshi Kanojo (32655)
        18. Dousei Lover Able (7774)
        19. Zutto Sukishite Takusan Sukishite (11712)
        20. Katawa Shoujo (945)
        21. Sugar * Style (24320)
        22. Haji Kano ~Kimi ga Iru Heya~ (27070)
        23. Deatte 5-fun wa Ore no Mono! Jikan Teishi to Atropos (23388)
        24. My Klutzy Cupid (31002)
        25. Amakano 2 (26307)
}
```
        
</details>

<details>
        
<summary>Characters Recommendations</summary>

### Touma Kazusa (White Album 2)
```
Enter the Char ID: 12973
Recommendations for Touma Kazusa (12973) gender_match=True, exclude_same_vns=True:
Traits:
{
        1. Hazuki Shizuku (53448) with score 0.384
                - Tsukiakari ni Modaeru Harame (20105)

        2. Narusawa Rikka (19051) with score 0.382
                - Hoshi Ori Yume Mirai (14265)
                - Hoshi Ori Yume Mirai - Rikka to Anata no 1-Shuunen Kinen, Icha Love Birthday (28160)

        3. Kinoshita Uzuki (85348) with score 0.382
                - Aikotoba (26537)

        4. Sakuragi Roofolet Ashe (37365) with score 0.374
                - WAGAMAMA HIGH SPEC (17823)
                - Wagamama High Spec OC (20524)

        5. Ichinose Honami (35679) with score 0.368
                - Amakano ~Second Season~ (17843)
                - Amakano+ (19810)
                - Amakano ~Second Season~+ (21675)
                - Amakano 2+ (31813)

        6. Amanogawa Saya (35176) with score 0.365
                - A Sky Full of Stars (16560)
                - A Sky Full of Stars -Fine Days- (18907)
                - Miagete Goran, Yozora no Hoshi o: Interstellar Focus (22303)

        7. Yanagihara Ai (7479) with score 0.365
                - Hajimete Doushi 2 ~Happy Bakappuru~ (7142)

        8. Ayase Aisa (98081) with score 0.363
                - Sousaku Kanojo no Ren'ai Koushiki (31136)

        9. Ichinose Ayako (65052) with score 0.363
                - HarmonEy (22075)

        10. Kagaya Yuna (92165) with score 0.362
                - Renai X Royale - Love's a Battle (28633)
                - Ren'ai x Royale - Nonoka & Renna & Yuna Mini After Story (30238)
                - Ren'ai x Royale - Mari & Shione & Ao Mini After Story (30239)

        11. Habane Kotori (9333) with score 0.362
                - If My Heart Had Wings (9093)
                - If My Heart Had Wings -Flight Diary- (10979)
                - Kono Oozora ni, Tsubasa o Hirogete: snow presents (14812)

        12. Isurugi Yuki (54972) with score 0.361
                - Niizuma LOVELY x CATION (20406)

        13. Morisumi Ichika (75143) with score 0.358
                - Sugar * Style (24320)
                - Sugar*Style Koibito Ijou Fuufu Miman After Story!! (25813)

        14. Kisugi Tsukimi (54843) with score 0.354
                - Trouble Days (680)

        15. Kurusu Yukako (54160) with score 0.354
                - Ninki Seiyuu: How to Make a Pop Voice Actress (20148)
                - Boku no Mirai wa, Koi to Kakin to. ~Charge To The Future~ (24275)

        16. Kirishima Ayame (19696) with score 0.354
                - Yankee Kanojo to Kozukuri Gakuen Life ~Suki to ka Iuna! Buttobasu zo! Omae no Aka-chan Hoshikunacchimau Darou ga…~ (12493)

        17. Aritagawa Nio (71927) with score 0.354
                - Loca-Love: My Cute Roommate (23067)
                - Loca Love: My Commuting Crush (25690)
                - Loca-Love: My Pure Priestess (26376)

        18. Amahara Sayuri (41443) with score 0.354
                - Ane wa Kanojo de Senzoku Maid (7656)

        19. Wataribe Kyouka (92988) with score 0.354
                - Ichizu na Kanojo to Koi Shitai (29195)
                - Ichizu na Kanojo to Koi Shitai ver. Hirohashi Runa (34410)

        20. Sakuragibashi Rito (65602) with score 0.352
                - Karigurashi Ren'ai (22045)

        21. Houjouin Seika (9857) with score 0.351
                - Princess Lover! (765)

        22. Kibitsumiya Akari (8445) with score 0.351
                - Onigokko! (5549)
                - Onigokko! Fandisc (7625)

        23. Tsujidou Ai (5398) with score 0.351
                - Tsujidou-san no Jun'ai Road (9879)
                - Tsujidou-san no Virgin Road (12283)
                - Maji de Watashi ni Koishinasai!! Spark (20012)
                - Minato Carnival FD (21122)

        24. Hiiragi Mio (34046) with score 0.35
                - Koi Suru Kimochi no Kasanekata (17632)
                - Koi Suru Kimochi no Kasanekata ~Kasaneta Omoi o Zutto~ (19104)

        25. Byakudan Midori (9765) with score 0.349
                - Kanojo x Kanojo x Kanojo ~Sanshimai to no Dokidoki Kyoudou Seikatsu~ (702)
                - Kanojo x Kanojo x Kanojo Dokidoki Full Throttle! (1442)

}
```

### Kurashina Asuka (Aokana)
```
Enter the Char ID: 22767
Recommendations for Kurashina Asuka (22767) gender_match=True, exclude_same_vns=True:
Traits:
{
        1. Hirosawa Hikari (35644) with score 0.469
                - Under One Wing (17827)

        2. Himeno Sena (33047) with score 0.435
                - Koi x Shin Ai Kanojo (17516)

        3. Hayakawa Natsuo (1572) with score 0.43
                - Nagisa no (401)

        4. Suzumori Ichika (60725) with score 0.414
                - Bishoujo Mangekyou -Tsumi to Batsu no Shoujo- (19182)

        5. Tachibana Nonoka (54732) with score 0.409
                - Anata ni Koi Suru Ren'ai Recette (20315)

        6. Tsukigase Mahiru (36311) with score 0.402
                - Sorairo Innocent (17980)

        7. Ursule Fleur Jeanmaire (9484) with score 0.398
                - Tsuki ni Yorisou Otome no Sahou (10680)
                - Otome Riron to Sono Shuuhen -Ecole de Paris- (12246)
                - Otome Riron to Sono go no Shuuhen -Belle Epoque- (18130)

        8. Nagamine Mikuri (49260) with score 0.398
                - Amenity's Life (19609)

        9. Kotomiya Chinatsu (10399) with score 0.398
                - Lover Able (5734)
                - Dousei Lover Able (7774)

        10. Migita Hibiki (39200) with score 0.398
                - Maitetsu (18131)
                - Maitetsu - Last Run!! (25635)

        11. Otonashi Ophilia Reo (15019) with score 0.397
                - Loveressive (11052)

        12. Himenomiya Miharu (8968) with score 0.397
                - Step×Steady (265)
                - ~Koidamazume~ (4061)

        13. Koyurugi Yurugi (55651) with score 0.393
                - Suisou Ginka no Istoria (20471)

        14. Hoshimi Tsukuyo (16389) with score 0.39
                - Kiss Ato (13632)
                - Ai Kiss (26180)

        15. Suzushiro Nanami (11474) with score 0.389
                - Skyprythem (2624)

        16. Higuchi Yumi (28351) with score 0.389
                - memories (2914)

        17. Kakogawa Mirai (3687) with score 0.387
                - Four-leaf (1590)

        18. Otowa Mizuki (42929) with score 0.387
                - Areas ~Koi Suru Otome no 3H~ (3817)

        19. Aria Celestia (34617) with score 0.384
                - Unlucky Re:Birth/Reverse (17560)

        20. Hatsushiba Kisa (655) with score 0.383
                - Diamic Days (6671)

        21. Yuuki Haruna (1188) with score 0.383
                - FORTUNE ARTERIAL (87)

        22. Sendou Erika (1186) with score 0.382
                - FORTUNE ARTERIAL (87)

        23. Ogura Minamo (27294) with score 0.381
                - Dolphin Divers (9916)

        24. Isshi Mizuki (20421) with score 0.38
                - Ame Koi (15426)

        25. Kawakami Kazuko (3508) with score 0.379
                - Majikoi! Love Me Seriously!! (1143)
                - Maji de Watashi ni Koishinasai! S (6245)
                - Maji de Watashi ni Koishinasai! Drama CD (16539)
                - Maji de Watashi ni Koishinasai! A-1 (20598)
                - Maji de Watashi ni Koishinasai! A-2 (20599)
                - Maji de Watashi ni Koishinasai! A-3 (20600)
                - Maji de Watashi ni Koishinasai! A-4 (20601)
                - Maji de Watashi ni Koishinasai! A-5 (20602)
                - Maji de Watashi ni Koishinasai! A Plus Disk (20604)
                - Minato Carnival FD (21122)

}
```

### Kaguya Riho (DEARDROPS)
```
Enter the Char ID: 5243
Recommendations for Kaguya Riho (5243) gender_match=True, exclude_same_vns=True:
Traits:
{
        1. Misumi Chisa (15001) with score 0.429
                - Kimi to Issho ni (7608)

        2. Abe Kimiko (2975) with score 0.425
                - Back Stage (845)

        3. Igano Rin (8248) with score 0.421
                - Hachimitsu Otome Blossomdays (2617)

        4. Koganei Tamaki (44371) with score 0.408
                - A Sky Full of Stars -Fine Days- (18907)
                - Miagete Goran, Yozora no Hoshi o: Interstellar Focus (22303)

        5. Yuminaga Misaki (33077) with score 0.404
                - Meguru Kisetsu no Yakusoku to, Tsunaida Sono Te no Nukumori to (12027)

        6. Sudou Kana (45733) with score 0.391
                - Shikotama Slave ~Aruji de Shimai na Tenshi to Akuma~ (2199)

        7. Inagaki Miyuu (7732) with score 0.391
                - Manbiki, Dame. Zettai!! ~Seiso na Manbiki Joshi - Class Zen'in 2-hon Sashi! Double ω Keikaku~ (5119)

        8. Josette Calicio (23961) with score 0.389
                - Kyonyuu Try! -Tanki Shuuchuu Chichi Momi Lesson- (6591)

        9. Sasameki Urumi (38704) with score 0.389
                - Koi ☆ Katsu! (6366)

        10. Mikogami Haruruko (34624) with score 0.389
                - Royal Garden ~Otome ni Koi Suru Ouji no Gikyoku~ (17826)

        11. Ayase Natsuki (22471) with score 0.384
                - Sakaagari Hurricane - Let's Pile Up Our School!! (1199)

        12. Mitamura Karen (43363) with score 0.382
                - School Love! 2 ~Koi Suru Parfaittic~ (1659)
                - School Love! ~Soyokaze no Harmony~ (5721)

        13. Omigawa Nadeshiko (31219) with score 0.382
                - Kiss x 800 ~Kiss de Gakuen Houkai? Houkago Hen~ (12220)
                - Kiss x 800 ~Kiss de Gakuen Houkai? Okujou Hen~ (12847)

        14. Akiyama Ryouka (15029) with score 0.382
                - Kimi to Issho ni 2 (13334)

        15. Elizabeth Oshiro (46109) with score 0.381
                - Lucid9 (16156)

        16. Takatoo Nanase (2522) with score 0.379
                - Kakyuusei 2 (1083)
                - Elf All Stars Datsui Jan 3 (2296)

        17. Kanzaki Karen (3386) with score 0.379
                - Meitantei Shikkaku na Kanojo (2197)

        18. Kitami Rin (77297) with score 0.379
                - Sakura Iro, Mau Koro ni (24650)

        19. Natsu Natsuki (10032) with score 0.373
                - Chu→ning Lover (10026)

        20. Shamrock (80088) with score 0.368
                - SPIRAL!! (24748)

        21. Ayanokouji Ouka (23716) with score 0.368
                - Higyaku Ms ~Seieki Shiboritoranaide!~ (2217)

        22. Yuuki Hikari (9673) with score 0.368
                - Sore wa Maichiru Sakura no You ni (1115)
                - Sore wa Maichiru Sakura no You ni (1115)
                - Sore wa Maichiru Sakura no You ni (1115)

        23. Koizumi Yuzuki (20660) with score 0.367
                - Resign (7958)

        24. Kumoi Akari (9341) with score 0.365
                - If My Heart Had Wings (9093)
                - If My Heart Had Wings -Flight Diary- (10979)
                - If My Heart Had Wings -Flight Diary- (10979)
                - If My Heart Had Wings -Flight Diary- (10979)
                - If My Heart Had Wings -Flight Diary- (10979)

        25. Kira Rin (33185) with score 0.365
                - Sakaagari Hurricane - Let's Pile Up Our School!! (1199)
                - Sakaagari Hurricane - Let's Pile Up Our School!! (1199)
                - Sakaagari Hurricane - Let's Pile Up Our School!! (1199)
                - Sakaagari Hurricane - Let's Pile Up Our School!! (1199)

}
```

### Sakaki Yumiko (Fruit of Grisaia)
```
Enter the Char ID: 569
Recommendations for Sakaki Yumiko (569) gender_match=True, exclude_same_vns=True:
Traits:
{
        1. Shinozaki Marika (19045) with score 0.417
                - Hoshi Ori Yume Mirai (14265)

        2. Ichinose Mirai (19162) with score 0.417
                - Koi iro Chu! Lips (4017)

        3. Narusawa Rikka (19051) with score 0.406
                - Hoshi Ori Yume Mirai (14265)
                - Hoshi Ori Yume Mirai - Rikka to Anata no 1-Shuunen Kinen, Icha Love Birthday (28160)

        4. Natsushima Misaki (17530) with score 0.394
                - Namaiki Delation (12288)

        5. Yotsuba Kohaku (87164) with score 0.382
                - Ore no Sugata ga, Toumei ni!? Invisible to Suuki na Unmei (26989)

        6. Oribe Kokoro (45355) with score 0.377
                - Amatsutsumi (18852)

        7. Kurahashi Seira (88382) with score 0.37
                - Tsuki no Kanata de Aimashou (24803)
                - Tsuki no Kanata de Aimashou: SweetSummerRainbow (26485)

        8. Asagiri Kasumi (92066) with score 0.37
                - Saimin Datsujo ~Subete ga Boku no Jiyuu ni Naru Sekai e Youkoso~ Asagiri Kasumi Hen (28884)

        9. Shima Sako (38260) with score 0.37
                - Omae no Pantsu wa Nani-iro da!? (7939)

        10. Sakuragibashi Rito (65602) with score 0.365
                - Karigurashi Ren'ai (22045)

        11. Akitsuki Shiho (58414) with score 0.364
                - Toshishita Gentei Nuki x2 Share-house ~Shiborare Kyoudou Seikatsu~ (20663)

        12. Shiina Miyako (3509) with score 0.362
                - Majikoi! Love Me Seriously!! (1143)
                - Maji de Watashi ni Koishinasai! S (6245)
                - Maji de Watashi ni Koishinasai! Drama CD (16539)
                - Maji de Watashi ni Koishinasai! A-1 (20598)
                - Maji de Watashi ni Koishinasai! A-2 (20599)
                - Maji de Watashi ni Koishinasai! A-3 (20600)
                - Maji de Watashi ni Koishinasai! A-4 (20601)
                - Maji de Watashi ni Koishinasai! A-5 (20602)
                - Maji de Watashi ni Koishinasai! A Plus Disk (20604)
                - Minato Carnival FD (21122)

        13. Izumi Wakoto (12592) with score 0.361
                - LOVELY×CATION2 (10288)

        14. Yuuri Shachi (40409) with score 0.36
                - The Princess, the Stray Cat, and Matters of the Heart (18148)
                - The Princess, the Stray Cat, and Matters of the Heart 2 (19841)

        15. Yoshinoya Seine (12591) with score 0.358
                - LOVELY×CATION2 (10288)

        16. Tokiwa Kano (87838) with score 0.357
                - Hamidashi Creative (27449)
                - Hamidashi Creative Totsu (33205)

        17. Kiritou Kureha (41745) with score 0.355
                - Sakuranomori Dreamers (18760)
                - Sakura no Mori † Dreamers 2 (20264)

        18. Mizunose Kotori (17040) with score 0.352
                - AstralAir no Shiroki Towa (12984)
                - AstralAir no Shiroki Towa Finale -Shiroki Hoshi no Yume- (19294)

        19. Ishigaki Yukari (69254) with score 0.352
                - Natsu Koi! (21494)

        20. Hinamori Sakurako (79206) with score 0.348
                - Heroine wa Tomodachi Desu ka? Koibito Desu ka? Soretomo Tomefure Desu ka? (25124)

        21. Ichinose Iori (45931) with score 0.347
                - Yakimochi Kanojo no Ichizu na Koi (19274)

        22. Kanna Kana (20426) with score 0.346
                - PRIMAL HEARTS (14887)
                - PRIMAL HEARTS 2 (17038)

        23. Maisaka Mai (77388) with score 0.345
                - Study § Steady (24689)
                - Study § Steady 2 (32624)

        24. Akitsushima Chihaya (23851) with score 0.344
                - Hachinin no Mazokko (14932)

        25. Asahina Hinata (92312) with score 0.343
                - Koinoha -Koi no Share House- (29005)

}
```

### Kazami Yuuki (Fruit of Grisaia)
```
Enter the Char ID: 567
Recommendations for Kazami Yuuji (567) gender_match=True, exclude_same_vns=True:
Traits:
{
        1. Toubu Kaito (891) with score 0.444
                - Hello, Goodbye (5316)

        2. Mutsura Yuuto (5457) with score 0.411
                - DRACU-RIOT! (8213)

        3. Kakei Kyoutarou (9360) with score 0.411
                - Daitoshokan no Hitsujikai (8158)
                - Daitoshokan no Hitsujikai -Dreaming Sheep- (12480)

        4. Chitose Haruki (908) with score 0.411
                - Tenshin Ranman Lucky or Unlucky!? (1322)

        5. Haruna Riku (24584) with score 0.407
                - AstralAir no Shiroki Towa (12984)
                - AstralAir no Shiroki Towa Finale -Shiroki Hoshi no Yume- (19294)

        6. Mizuwa Akihito (1435) with score 0.406
                - Coμ -Black Dragon in a Gentle Kingdom- (1896)

        7. Yanagise Chouji (12295) with score 0.402
                - Ikinari Anata ni Koishiteiru (5240)

        8. Sawai Tooru (5502) with score 0.401
                - Monobeno (8435)
                - Monobeno -Happy End- (12392)
                - Maitetsu (18131)

        9. Isac (109816) with score 0.396
                - My Real Desire (33014)

        10. Tsuchimi Rin (4671) with score 0.396
                - SHUFFLE! (28)
                - Tick! Tack! (201)
                - Really? Really! (202)
                - SHUFFLE! Love Rainbow (6427)
                - Navel * Plus (8664)
                - Shuffle! Essence+ Tokuten Disk (12525)
                - Princess x Princess (30216)

        11. Caim Astraea (515) with score 0.39
                - Aiyoku no Eustia (3770)

        12. Tachibana Kazuma (50252) with score 0.389
                - Mysteries of the Heart: The Psychic Detective Case Files (19684)

        13. Naoe Yamato (3885) with score 0.387
                - Majikoi! Love Me Seriously!! (1143)
                - Maji de Watashi ni Koishinasai! S (6245)
                - Tsujidou-san no Jun'ai Road (9879)
                - Maji de Watashi ni Koishinasai! Drama CD (16539)
                - Maji de Watashi ni Koishinasai!! Spark (20012)
                - Maji de Watashi ni Koishinasai! A-1 (20598)
                - Maji de Watashi ni Koishinasai! A-2 (20599)
                - Maji de Watashi ni Koishinasai! A-3 (20600)
                - Maji de Watashi ni Koishinasai! A-4 (20601)
                - Maji de Watashi ni Koishinasai! A-5 (20602)
                - Maji de Watashi ni Koishinasai! A Plus Disk (20604)
                - Maji de Watashi ni Koishinasai! A - Ryouken Route After (27092)

        14. Okonogi Masaya (3103) with score 0.386
                - Princess Evangile (6710)
                - Princess Evangile W Happiness (8900)

        15. Nonomura Yuuto (36919) with score 0.386
                - Tsumi no Hikari Rendezvous (17872)
                - Tsumi no Hikari Rendezvous: Mikan Blossom (37380)

        16. Yagami Yuuichi (4446) with score 0.383
                - Hara ☆ Kano!! ~Ano Ko to Lovelove Harabote Seikatsu~ (2736)

        17. Arichi Masaomi (49563) with score 0.38
                - Senren＊Banka (19073)

        18. Kita Chihaya (41322) with score 0.38
                - Puramai Wars (16339)

        19. Kaburagi Ayumu (36958) with score 0.379
                - Material Brave (7633)
                - Material Brave Ignition (10834)

        20. Ayatsuji Hinata (55124) with score 0.379
                - Samidare Growing Up! (17985)

        21. Azai Kyousuke (305) with score 0.378
                - G-senjou no Maou - The Devil on G-String (211)
                - G-Senjou no Maou - Dai Bangaihen "Sharin no Kuni no Maou" (20273)

        22. Shirosaki Joutarou (22700) with score 0.377
                - Kashimashi Communication (2908)

        23. Tsushima Reo (60) with score 0.376
                - Tsuyokiss (397)
                - Tsuyokiss 2gakki (398)
                - Minikiss ~Tsuyokiss Fan Disc~ (399)
                - Tsuyokiss 3gakki (6173)
                - Tsuyokiss FESTIVAL (18005)

        24. Saegusa Kazuki (12489) with score 0.375
                - Hitotsu Tobashi Ren'ai (11300)

        25. Fujima Ren (44410) with score 0.375
                - The Ditzy Demons Are in Love With Me (17515)
                - The Ditzy Demons Are in Love With Me - Fandisc (18791)

}
```

### Saya (Saya no Uta)
```
Enter the Char ID: 66
Recommendations for Saya (66) gender_match=True, exclude_same_vns=True:
Traits:
{
        1. Azuma Ruka (16301) with score 0.347
                - 3days ~Michiteyuku Toki no Kanata de~ (1085)

        2. Kouzuki Kazuna (16799) with score 0.333
                - Cartagra ~Affliction of the Soul~ (515)
                - Nagomibako Innocent Grey Fandisc (916)

        3. Amase Hikaru (48604) with score 0.33
                - Koakuma Hatsuiku Chu~! (19495)

        4. Ai (51515) with score 0.308
                - L.i.n.k. -Kimyou na Unmei ni Tsunagareta Monotachi no, Chi to Namida no Uta- (2221)

        5. Amagasa Hikari (12950) with score 0.3
                - Tamahaji! -Tamatama Hajikeru Imouto-tachi- (12565)

        6. Imazato Koyomi (60634) with score 0.297
                - Niizuma Koyomi (20515)

        7. Sora (119969) with score 0.294
                - Stellar ☆ Theater (1185)

        8. Sawatari Nanagi (10714) with score 0.293
                - Aete Mushi Suru Kimi to no Mirai ~Relay Broadcast~ (10803)

        9. Serizawa Mizuho (34362) with score 0.293
                - Love Letter (4948)

        10. Motai Ikue (26715) with score 0.291
                - Bijukubo "Iyarashii Kaa-san de Gomenne..." (1994)

        11. Kagurazaka Ikoi (43473) with score 0.289
                - JOKER -Shisen no Hate no Doukeshi- (10448)

        12. Sagisawa Karen (48545) with score 0.289
                - Ero Zemi ~Ecchi ni Yaru-ki ni ABC~ (19391)

        13. Kuragano Hitoha (66245) with score 0.288
                - Kahogo de Ecchi na Boku no Ane (22245)

        14. Kumagai Haruka (87959) with score 0.286
                - Sukebe na Shojo no Tsukurikata (27523)

        15. Yurifina Sol Eleanord (23383) with score 0.286
                - Unionism Quartet (15288)
                - Unionism Quartet A3-Days (18882)

        16. Shirogo Nami (40489) with score 0.286
                - Play! Play! Play! Shi (16935)

        17. Miyama Rina (48601) with score 0.283
                - Koakuma Hatsuiku Chu~! (19495)

        18. Sakihara Rin (55771) with score 0.282
                - Chiccha na Hanayome ~Mada Mada Tsubomi da mon~ (20284)

        19. Sakamaki Yukiho (23106) with score 0.278
                - Meidokissa. (16081)

        20. Ayasaki Nanoka (21436) with score 0.277
                - Hare Nochi Kitto Nanohana Biyori (14886)

        21. Great Sage (105267) with score 0.275
                - All Demons go to Heaven (34200)

        22. Nakanokouji Ayano (12192) with score 0.274
                - Genmukan ~Aiyoku to Ryoujoku no Inzai~ (772)
                - Shinshou Genmukan (2605)

        23. Momo (24930) with score 0.274
                - Bunny Black 2 (8192)

        24. Uzuki Saki (24617) with score 0.273
                - Sakura Synchronicity (16215)

        25. Maya (31871) with score 0.273
                - Triptych (537)

}
```

### Rance (Rance X)
```
Enter the Char ID: 735
Recommendations for Rance (735) gender_match=True, exclude_same_vns=True:
Traits:
{
        1. Rance (52689) with score 0.478
                - Toushin Toshi II (889)
                - Rance: Quest for Hikari (1414)
                - Rance II - Hangyaku no Shoujo-tachi - (1427)
                - Rance III - The Fall of Leazas - (1829)
                - Kichikuou Rance (2045)

        2. N/A (95156) with score 0.327
                - Fantasy Tavern Sextet -Vol.1 New World Days- (29482)
                - Fantasy Tavern Sextet -Vol.2 Adventurer's Days- (31090)
                - Fantasy Tavern Sextet -Vol.3 Postlude days- (31091)

        3. Kotetsu (116620) with score 0.327
                - Isekai Erect (38822)

        4. Emilio (16871) with score 0.322
                - Himegari Dungeon Meister (1195)
                - Ikusa Megami Verita (2836)
                - Soukoku no Arterial (8424)

        5. Darks (22342) with score 0.313
                - Bunny Black (3947)
                - Bunny Black 2 (8192)
                - Bunny Black 3 (12186)

        6. Handa Nora (40411) with score 0.306
                - The Princess, the Stray Cat, and Matters of the Heart (18148)
                - The Princess, the Stray Cat, and Matters of the Heart 2 (19841)

        7. Nulkan (95753) with score 0.293
                - Shuggerlain (30407)

        8. Weissheit Zerinder (19830) with score 0.289
                - Madou Koukaku ~Yami no Tsuki Megami wa Doukoku de Utau~ (11620)

        9. Louie Marcillen (31110) with score 0.288
                - Ikusa Megami Verita (2836)
                - Fuukan no Grasesta (23199)

        10. Protagonist (5167) with score 0.287
                - Eiyuu Senki - The World Conquest (6458)
                - Eiyu*Senki Gold - A New Conquest (12033)

        11. Sakagami Habaki (34796) with score 0.286
                - Dies irae ~Acta est Fabula~ (548)
                - Kajiri Kamui Kagura (5844)

        12. Daijuuji Kurou (931) with score 0.284
                - Deus Machina Demonbane (231)

        13. Sugisawa Reiji (17172) with score 0.282
                - Ura Kyoushi ~Haitoku no In'etsu Jugyou~ (7442)

        14. TetuOne (11897) with score 0.278
                - Shichinin no Online Gamers ~Offline~ (545)

        15. Hongou Kazuto (63854) with score 0.278
                - Shin Koihime † Musou ~Otome Ryouran ☆ Sangokushi Engi~ (1967)
                - Shin Koihime † Musou ~Moeshouden~ (3987)
                - Sengoku † Koihime ~Otome Kenran ☆ Sengoku Emaki~ (13188)
                - Shin Koihime † Eiyuutan (16463)
                - Shin Koihime † Musou -Kakumei- Souten no Haou (18649)
                - Shin Koihime † Musou -Kakumei- Son Go no Ketsumyaku (20591)
                - Shin Koihime † Musou -Kakumei- Ryuuki no Taimou (20592)
                - Shin Koihime † Eiyuutan 4 ~Otome Enran ☆ Sangokushi Engi [Go]~ (31814)
                - Shin Koihime † Eiyuutan 5 ~Otome Enran ☆ Sangokushi Engi [Gi]~ (31815)
                - Shin Koihime † Eiyuutan - Gaiden - Shiratsuki no Tomoshibi (31817)

        16. Alex (111218) with score 0.277
                - Trouble in Paradise (36700)

        17. Miyabi Kurou (2048) with score 0.276
                - Idols Galore! (141)
                - Motto Muriyari! (6086)
                - Ohime-sama o Otose! (6620)

        18. Caim Astraea (515) with score 0.275
                - Aiyoku no Eustia (3770)

        19. Koji Takei (105086) with score 0.275
                - Takei's Journey (34166)

        20. Mimori Ichirou (32325) with score 0.274
                - Hatsumira -from the future undying- (15080)

        21. Touma Taiga (8673) with score 0.273
                - DUEL SAVIOR (309)
                - Otome Crisis (479)
                - Xross Scramble (491)

        22. Protagonist (88192) with score 0.273
                - HaremKingdom (26765)
                - Harem ja Nai yo Kingdom - Hikari & Sophia & Kiki Hen (28825)
                - Harem ja Nai yo Kingdom - Charlone & Marrou Hen (28881)

        23. Urabe Keisuke (8926) with score 0.272
                - Onigokko! (5549)
                - Onigokko! Fandisc (7625)

        24. Nick (110176) with score 0.272
                - Devilish Business (36379)

        25. Hoshikawa Sorata (58405) with score 0.272
                - Yozora Rhapsody (20348)

}
```

### Monika (Doki Doki Literature Club)
```
Recommendations for Monika (64502) gender_match=True, exclude_same_vns=True:
Traits:
{
        1. Monika (68457) with score 0.801
                - Doki Doki! RainClouds (22637)
                - Doki Doki! New Eyes (23036)

        2. Monicules (69024) with score 0.49
                - Doki Doki Do You Lift Club! (22717)

        3. Monika (69672) with score 0.479
                - Doki Doki School Club (22824)

        4. Monika (91063) with score 0.471
                - Doki Doki Blue Skies (28556)

        5. Monika (70506) with score 0.452
                - Doki Doki Literature Club 2 Next History (22971)

        6. Kuresato Nagi (43133) with score 0.438
                - Dear Pianissimo (674)

        7. Suzunari Rinko (26413) with score 0.426
                - Kamitsure ~7 no Nijou Fushigi~ (15731)

        8. Aoki Minami (12891) with score 0.415
                - Ryoujoku Sensei (5921)

        9. Takase Kyouka (11563) with score 0.415
                - Okitsune-sama no Koisuru Omajinai (3865)

        10. Sawada Ruri (46639) with score 0.409
                - Naisho no Tintin Time (1735)

        11. Yuri (68454) with score 0.409
                - Doki Doki! RainClouds (22637)
                - Doki Doki! New Eyes (23036)

        12. Ziva Shani (45622) with score 0.405
                - One Thousand Lies (19014)

        13. Shibamiya Rina (43974) with score 0.403
                - Amaekata wa Kanojo Nari ni. (18335)

        14. Yukiwa Fuuka (33279) with score 0.402
                - Onna no Ko wa Do S na Hentai de Dekiteiru (17342)

        15. Sheila El Elise (34278) with score 0.402
                - Maji Suki ~Marginal Skip~ (1140)

        16. Nanase Ririko (33540) with score 0.402
                - Mahou Senshi Extra Stage ~10th Anniversary~ (11135)

        17. Hayase Misora (24412) with score 0.402
                - Yokujou Zecchou Love Drug ~Akogare no Bishoujo ga Ore ni Omata Hiraite Ecchi no Onedari~ (12833)

        18. Akaba Chizuru (67838) with score 0.395
                - Seitokai no Ichizon - DS Suru Seitokai (3209)
                - Seitokai no Ichizon Lv.2 Portable (26748)

        19. Natsumi (77609) with score 0.395
                - 120 Yen no Haru (2585)

        20. Hinomiya Matsuri (119874) with score 0.395
                - Real Eroge Situation! DT (39872)

        21. Chitose Mizuki (54948) with score 0.392
                - Angel Wish ~Houkago no Meshitsukai ni Chu!~ (1176)

        22. Kajiwara Hinako (91191) with score 0.392
                - Hare Tokidoki Otenkiame (5193)

        23. Tomosaka Rina (46635) with score 0.392
                - Naisho no Tintin Time (1735)

        24. Aiba Erika (52070) with score 0.389
                - Tenshitsuki no Shoujo (1039)

        25. Kay (68413) with score 0.389
                - Odd Love Test (22631)

}
```

### Yuri (Doki Doki Literature Club)
```
Recommendations for Yuri (64504) gender_match=True, exclude_same_vns=True:
Traits:
{
        1. Yuri (68454) with score 0.917
                - Doki Doki! RainClouds (22637)
                - Doki Doki! New Eyes (23036)

        2. Yuronk (69025) with score 0.475
                - Doki Doki Do You Lift Club! (22717)

        3. Yuri (91066) with score 0.44
                - Doki Doki Blue Skies (28556)

        4. Onose Ayame (47745) with score 0.402
                - Triangle Love -Apricot Fizz- (19445)

        5. Yui (69669) with score 0.402
                - Japan Book High School Club Dating Simulator (22751)

        6. Shizuru (34761) with score 0.396
                - Tsun na Kanojo Dere na Kanojo (1336)

        7. Monika (68457) with score 0.388
                - Doki Doki! RainClouds (22637)
                - Doki Doki! New Eyes (23036)

        8. Shirakawa Iori (18221) with score 0.385
                - uni. (4253)

        9. Sakurano Honoka (65291) with score 0.384
                - White Princess (3039)
                - White Princess (3039)

        10. Senpai (73837) with score 0.379
                - Monochro no Umi o Tadayou Hito (23938)

        11. Kunashi Hatsuka (36728) with score 0.379
                - Kotowari ~Kimi no Kokoro no Koboreta Kakera~ (6918)

        12. Sumizato Kiwako (23962) with score 0.378
                - Kyonyuu Try! -Tanki Shuuchuu Chichi Momi Lesson- (6591)

        13. Sasaki Kaoru (11309) with score 0.377
                - Maple Colors 2 (1285)

        14. Sayori (68455) with score 0.377
                - Doki Doki! RainClouds (22637)
                - Doki Doki! New Eyes (23036)

        15. Kariya Yuki (27459) with score 0.377
                - Tozasareta In'yoku no Gakuen (11962)

        16. Yabusame Kaname (33811) with score 0.377
                - Kurui no Tsuki (17692)

        17. Kujou Akane (22924) with score 0.377
                - Onegai Tasukete!! 2 ~Sosogare Tsuzukeru Seieki~ (14141)

        18. Kuriyama Natsuko (55024) with score 0.377
                - Sakura no Uta -Sakura no Mori no Ue o Mau- (562)
                - Sakura no Toki -Sakura no Mori no Shita o Ayumu- (20431)

        19. Hoshioki Marika (32129) with score 0.377
                - Hyakugojuunenme no Mahoutsukai (15408)

        20. Hazuki Chika (4993) with score 0.367
                - Aikagi ~Hidamari to Kanojo no Heyagi~ (1270)

        21. Ou Kagetsu (24547) with score 0.367
                - Senjin Otome -Makina ni Yadorishi Kokoro ga Negau wa...- (12557)

        22. Lillian (40729) with score 0.367
                - Sepia Tears (8489)

        23. Miyazaki Nodoka (25381) with score 0.367
                - Mahou Sensei Negima! 1-Jikanme ~Okochama Sensei wa Mahou Tsukai!~ (2097)
                - Mahou Sensei Negima! 2-Jikanme ~Tatakau Otome-tachi! Mahora Daiundokai SP!~ (2098)

        24. Takachiho Sayo (16449) with score 0.365
                - The Shadows of Pygmalion (12072)

        25. Toujou Shion (47415) with score 0.362
                - Otome Smile (944)

}
```

### Shinozuka Yayoi (White Album)
```
Enter the Char ID: 58533
Recommendations for Shinozuka Yayoi (58533) gender_match=True, exclude_same_vns=True:
Traits:
{
        1. Takatsu Yukina (87779) with score 0.447
                - Toji no Miko: Kizamishi Issen no Tomoshibi (27434)

        2. Gamou Makiko (89327) with score 0.424
                - 7'scarlet (18162)

        3. Ooba Kaho (74001) with score 0.365
                - Sore Ike! Chinporter! ~Shinshutsukibotsu na Ore no Are~ (23315)

        4. Wisht (99921) with score 0.365
                - Methods: The Detective Competition (26007)

        5. Sora's Mother (113308) with score 0.335
                - Project: Perfectly Normal (29419)

        6. Nakamura (26060) with score 0.316
                - Milkyway 3 (6193)

        7. Kurosaki Yuu (102571) with score 0.316
                - School Festa (4438)

        8. Midorikawa Emu (108575) with score 0.316
                - Sweet Days (9103)

        9. Natasha (103661) with score 0.316
                - Luna's Fall From Grace (30352)

        10. Hazuki (119373) with score 0.316
                - Itazura Teacher ~Himitsu no Hokenshitsu~ (39917)

        11. Momoka (119374) with score 0.316
                - Ecchi na Himitsu Kichi 2 ~Kondo wa Kankinda~ (39918)

        12. Gein Spare Ribs (102013) with score 0.316
                - GUN GRAVE (33199)

        13. Okadama Natsuki (118296) with score 0.316
                - 300 Nen Buri no Chikyuu ni, Nake (39410)

        14. Kurenai (85581) with score 0.316
                - Net High (18943)

        15. Kozuka Hiroko (94861) with score 0.316
                - Owarinaki Natsu, Towa Naru Shirabe (1743)

        16. Nurse Furukawa (118658) with score 0.316
                - BLACK SHEEP TOWN (21069)

        17. Saegusa Akiko (77277) with score 0.316
                - Mama Shibori (6059)

        18. Girl (80695) with score 0.316
                - Daiku no Medium (25361)

        19. Nia Aphrodite (114452) with score 0.316
                - Luna Majogari (16457)

        20. Anna (80696) with score 0.316
                - Daiku no Medium (25361)

        21. Yoshie Sakura (56308) with score 0.316
                - Iinazuke (7008)

        22. Karin Okazaki (33099) with score 0.316
                - Switch - Fluch oder Segen (7827)
                - Alternate - Der Fall Okazaki (7828)

        23. Elmaria (101587) with score 0.316
                - Akikaze Yozora ~Boy Meets UFO~ (6423)

        24. Aihara Koyori (102473) with score 0.316
                - Dr. Peko Himitsu no Shinryoujo 2 ~Mamori no Himitsu Kaiketsu Itashimasu~ (9788)

        25. Abigail (105824) with score 0.316
                - University of Problems (32644)

}
```

</details>
