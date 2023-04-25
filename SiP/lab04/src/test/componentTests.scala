package componentTests

import cards._
import deck._
import cards._
import games._

object DeckTests {
  def testStandardDeck(): Unit = {
    assert(Deck().isStandard)
  }

  def testAmountOfColorInStandardDeck(): Unit = {
    assert(Deck().amountOfColor(Hearts) == 13)
  }

  def testAmountWithFaceInStandardDeck(): Unit = {
    val deck = Deck()
    assert(deck.amountWithFace == 12)
  }

  def testPullFirstCardInTheDeck(): Unit = {
    val king = Card(Hearts, King)
    val queen = Card(Hearts, Queen)
    val deck = new Deck(List(king, queen))

    val deckWithoutKing = deck.pull()
    assert(deckWithoutKing.amountOfFace(King) == 0)
  }

  def testPullMultipleTimes(): Unit = {
    val ace = Card(Hearts, Ace)
    val king = Card(Hearts, King)
    val queen = Card(Hearts, Queen)
    val cards = List(ace, king, queen)
    val deck = new Deck(cards)

    for (c <- cards)
      assert(deck.duplicatesOfCard(c) == 1)

    val deck1 = deck.pull()
    assert(deck.duplicatesOfCard(ace) == 0)
    val deck2 = deck1.pull()
    assert(deck2.duplicatesOfCard(king) == 0)
    val deck3 = deck2.pull()
    assert(deck3.duplicatesOfCard(queen) == 0)
  }

  def testPullEmptyDeck(): Unit = {
    val deck = new Deck(List())
    try {
      deck.pull()
      assert(false, "Pull card from empty deck did not yield an error")
    } catch {
      case _: EmptyDeckError => ()
    }
  }

  def testNoDuplicatesInDeck(): Unit = {
    val deck = new Deck(List())
    assert(deck.duplicatesOfCard(Card(Hearts, King)) == 0)
  }

  def testDuplicatesSingleCardInDeck(): Unit = {
    val card = Card(Hearts, Queen)
    val deck = new Deck(List(card))
    assert(deck.duplicatesOfCard(card) == 0)
  }

  def testDuplicatesMultipleCardInstances(): Unit = {
    val card = Card(Hearts, Queen)
    val deck = new Deck(List.fill(3)(card))
    assert(deck.duplicatesOfCard(card) == 2)
  }

  def runTests(): Unit = {
    // Pulling card from deck
    testPullFirstCardInTheDeck()
    testPullEmptyDeck()

    testStandardDeck()

    testNoDuplicatesInDeck()
    testDuplicatesSingleCardInDeck()
    testDuplicatesMultipleCardInstances()

    testAmountOfColorInStandardDeck()
    testAmountWithFaceInStandardDeck()
  }
}

object BlackjackTests {
  import games.Blackjack.prettyPrintCards

  def runTests(): Unit = {
    println("Testing All21 function")
    testAll21()
  }

  def testAll21(): Unit = {
    val cards = List(
      Card(Hearts, Numerical(7)),
      Card(Diamonds, Numerical(10)),
      Card(Hearts, Numerical(4)),
      Card(Spades, Ace),
      Card(Hearts, Ace),
      Card(Spades, Numerical(9)),
      Card(Diamonds, Ace)
    )
    prettyPrintCards(cards)

    val deck = new Deck(cards)
    val blackjack = new Blackjack(deck)

    val all21 = blackjack.all21

    for (list <- all21) {
      println("Hands: ")
      prettyPrintCards(list)
    }

    assert(all21.length == 3)
  }
}
