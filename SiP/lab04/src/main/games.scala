package games

import cards._
import deck.Deck

class Blackjack(deck: Deck) {
  import games.Blackjack.{evalCards, prettyPrintCards}
  // Points calculation:
  //  1. Numerical cards as their numerical value = 2 - 10.
  //  2. Face cards (Jack, Queen, King) = 10
  //  3. Ace = 1 or 11 (player could choose)

  // loop taking n cards from the deck, pretty-printing them with points
  // & printing the sum of points on the end
  def play(n: Int): Unit = {
    require(n > 0)

    val cards = deck.cards.take(n)
    val handValue = evalCards(cards)

    prettyPrintCards(cards)
    println(s"Hand value: $handValue")
  }

  // finds all subsequences of cards which could give 21 points
  lazy val all21: List[List[Card]] = {
    val size = deck.cards.length
    (for {
      from <- 0 to size
      until <- from + 1 to size

      cards = deck.cards.slice(from, until)
      if evalCards(cards) == 21
    } yield cards).toList
  }

  // finds and pretty-prints the first subsequence of cards which could give 21 points
  def first21(): Unit = prettyPrintCards(all21.head)
}

object Blackjack {
  private val target = 21
  private val aceMin = 1
  private val aceMax = 11

  // creates Blackjack game having numOfDecks-amount of standard decs with random order of cards
  def apply(numOfDecks: Int = 1): Blackjack = {
    import scala.util.Random.shuffle
    require(numOfDecks > 0)

    val cards = Deck.standardDeckCards.flatMap(x => List.fill(numOfDecks)(x))
    val deck = new Deck(shuffle(cards))
    new Blackjack(deck)
  }

  private def evalCard(card: Card, total: Int): Int = {
    card.rank match {
      case x: Numerical => x.value
      case _: Face      => 10
      case _: Ace       => if (total + aceMax > target) aceMin else aceMax
    }
  }

  private def evalCards(cards: List[Card], total: Int = 0): Int = {
    cards match {
      case Nil => total
      case card :: remainingCards =>
        val cardValue = evalCard(card, total)
        evalCards(remainingCards, total + cardValue)
    }
  }

  private def printCard(card: Card, cardValue: Int): Unit = {
    val rank = card.rank match {
      case Ace          => "A"
      case King         => "K"
      case Queen        => "Q"
      case Jack         => "J"
      case x: Numerical => x.value.toString()
    }

    val color = card.color match {
      case Hearts   => "♥"
      case Diamonds => "♦"
      case Clubs    => "♣"
      case Spades   => "♠"
    }

    println(s"${rank} ${color} [$cardValue]")
  }

  def prettyPrintCards(cards: List[Card], total: Int = 0): Unit =
    cards match {
      case Nil => ()
      case card :: otherCards =>
        val value = evalCard(card, total)
        printCard(card, value)
        prettyPrintCards(otherCards, total + value)
    }

}
