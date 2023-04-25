import games.Blackjack
import deck.Deck
import cards._

object Main extends App {

  def first21(): Unit = {
    val cards = List(
      Card(Spades, Ace),
      Card(Hearts, Ace),
      Card(Spades, Numerical(9)),
      Card(Diamonds, Ace)
    )
    val deck = new Deck(cards)
    val blackjack = new Blackjack(deck)

    blackjack.first21()
  }

  def blackjackPull(): Unit = {
    val blackjack = Blackjack()
    blackjack.play(4)
  }
  println("First 21:")
  first21()
  println("Play black jack")
  blackjackPull()
}
