package deck

import cards._
import scala.util.Random.shuffle

class EmptyDeckError extends Error

class Deck(val cards: List[Card]) {
  def pull(): Deck = {
    cards match {
      case Nil => throw new EmptyDeckError()
      case _   => new Deck(cards.tail)
    }
  }

  // creates new deck with given card pushed on top
  def push(card: Card): Deck = new Deck(card :: cards)

  // creates new deck with new card(color, value) pushed on top
  def push(color: Color, value: Rank): Deck = push(Card(color, value))
  // get amount of cards by given predicate
  private def getAmount(pred: Card => Boolean): Int = cards.filter(pred).size

  // checks if deck is a standard deck
  val isStandard: Boolean = {
    getAmount(Deck.standardDeckCards contains _) == Deck.standardDeckCards.size
  }

  // amount of duplicates of the given card in the deck
  def duplicatesOfCard(card: Card): Int = {
    val noCards = getAmount(_ == card)
    if (noCards > 0) noCards - 1 else 0
  }

  // amount of cards in the deck for the given color
  def amountOfColor(suit: Color): Int = getAmount(_.color == suit)

  // amount of cards in the deck for given numerical card (2, 3, 4, 5, 6, 7, 8, 9, 10)
  def amountOfNumerical(numerical: Numerical): Int = getAmount(
    _.rank == numerical
  )

  // amount of all numerical cards in the deck (2, 3, 4, 5, 6, 7, 8, 9, 10)
  val amountWithNumerical: Int = getAmount(_.rank.isInstanceOf[Numerical])

  // amount of cards in the deck for the given face (Jack, Queen & King)
  def amountOfFace(face: Face): Int = getAmount(_.rank == face)

  // amount of all cards in the deck with faces (Jack, Queen & King)
  val amountWithFace: Int = getAmount(_.rank.isInstanceOf[Face])
}

object Deck {
  val standardDeckCards: List[Card] = {
    val colors = List(Clubs, Diamonds, Spades, Hearts)
    val numericalRanks =
      (for (rank <- (2 to 10).toList) yield Numerical(rank))
    val ranks = List(Ace, Jack, Queen, King) ::: numericalRanks
    for {
      c <- colors
      r <- ranks
    } yield Card(c, r)
  }

  // creates the standard deck with random order of cards.
  def apply() = new Deck(shuffle(standardDeckCards))
}
