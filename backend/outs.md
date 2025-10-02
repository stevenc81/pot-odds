# **Verified Poker Outs Examples**

In poker, an **out** is defined as any unseen card remaining in the deck that, if drawn, will improve a player's hand to one that is likely to win the pot. This concept applies primarily in games with multiple betting rounds, such as Texas Hold'em or draw poker, where players calculate outs to estimate their chances of improving a drawing hand, like a flush or straight. For example, if a player holds four cards to a flush, there are typically nine outs (the remaining cards of that suit in the deck), assuming no visible cards reduce this number.

**Important Note:** Outs specifically refer to cards that can improve your **hole cards** (the private cards in your hand), not the community cards on the board. When calculating outs, you're determining which future community cards will combine with your existing hole cards to create a stronger hand. The community cards that are already revealed cannot be changed and are not considered when counting outs.

## **4 Outs Examples**

### **Inside Straight Draw (Gutshot)**
- **Hand:** 9♠ 8♥  
- **Board:** 5♣ 6♦ K♠  
- **Current:** Nine high  
- **Outs:** 7♠, 7♥, 7♦, 7♣  
- **Logic:** Need a 7 for straight (5-6-7-8-9)

### **Two Pair to Full House**  
- **Hand:** A♠ K♦  
- **Board:** A♥ K♠ 3♣  
- **Current:** Two pair (aces and kings)  
- **Outs:** A♦, A♣, K♥, K♣  
- **Logic:** Another ace or king completes full house

## **6 Outs Examples**

### **Two Overcards**
- **Hand:** A♠ K♦  
- **Board:** Q♣ 7♥ 2♠  
- **Current:** Ace high  
- **Outs:** A♥, A♦, A♣, K♠, K♥, K♣  
- **Logic:** Any ace or king makes top pair

## **7 Outs Examples**

### **Set to Full House or Quads**
- **Hand:** K♠ K♣  
- **Board:** 8♥ K♦ 3♠  
- **Current:** Three kings  
- **Outs:** 8♠, 8♦, 8♣, 3♥, 3♦, 3♣, K♥  
- **Logic:** Eights or threes for full house, K♥ for quads

### **Set with Full House Draw**
- **Hand:** 7♣ 7♠  
- **Board:** 7♥ A♦ K♠  
- **Current:** Three sevens  
- **Outs:** A♠, A♥, A♣ (aces full), K♥, K♦, K♣ (kings full), 7♦ (quads)  
- **Logic:** 3 aces + 3 kings + 1 seven = 7 outs

## **8 Outs Examples**

### **Open-Ended Straight Draw**
- **Hand:** 9♠ 8♥  
- **Board:** 7♣ 6♦ 2♠  
- **Current:** Nine high  
- **Outs:** 10♠, 10♥, 10♦, 10♣, 5♠, 5♥, 5♦, 5♣  
- **Logic:** Need 10 or 5 for straight

## **9 Outs Examples**

### **Flush Draw**
- **Hand:** A♠ K♠  
- **Board:** 7♠ 3♠ J♦  
- **Current:** Ace high with flush draw  
- **Outs:** Q♠, J♠, 10♠, 9♠, 8♠, 6♠, 5♠, 4♠, 2♠  
- **Logic:** Any remaining spade completes flush

### **Flush Draw (Alternative Example)**
- **Hand:** Q♥ 3♥  
- **Board:** 7♥ 9♣ K♥  
- **Current:** Queen high with flush draw  
- **Outs:** A♥, J♥, 10♥, 9♥, 8♥, 6♥, 5♥, 4♥, 2♥  
- **Logic:** Any remaining heart completes flush

## **11 Outs Examples**

### **Flush Draw + Set or Quads**
- **Hand**: 7♠ 7♦
- **Board**: K♠ 9♠ 4♠
- **Current**: Flush draw + pocket pair
- **Outs**: A♠, Q♠, J♠, 10♠, 8♠, 6♠, 5♠, 3♠, 2♠ (flush) + 7♥, 7♣ (set)
- **Logic**: 9 spades for flush + 2 sevens for set (no overlap since remaining 7s are hearts/clubs)

## **12 Outs Examples**

### **Flush Draw + One Overcard**
- **Hand:** A♠ 7♠  
- **Board:** 10♥ 6♠ 3♠  
- **Current:** Ace high with flush draw  
- **Outs:** 9 spades for flush + A♥, A♦, A♣ for top pair  
- **Logic:** 9 flush outs + 3 overcard outs = 12 total outs (no overlap since A♠ is already in hand)

### **Ace-High Flush Draw + Gutshot**
- **Hand:** A♥ 2♥  
- **Board:** K♥ T♥ Q♣  
- **Current:** Ace-high flush draw + gutshot straight draw  
- **Outs:** 9 hearts for flush + J♠, J♦, J♣ for straight  
- **Logic:** 9 flush outs (13 hearts − 4 seen) + 3 non-heart jacks (J♥ already counted in flush) = 12 outs

## **15 Outs Examples**

### **Straight Flush Draw**
- **Hand:** 10♠ 9♠  
- **Board:** 8♠ 7♥ 2♠  
- **Current:** Flush draw + open-ended straight draw  
- **Outs:** A♠, K♠, Q♠, J♠, 7♠, 6♠, 5♠, 4♠, 3♠ (flush) + J♥, J♦, J♣, 6♥, 6♦, 6♣ (straight)  
- **Logic:** 9 spades for flush + 6 non-spade cards for straight (minus 2 overlap)
