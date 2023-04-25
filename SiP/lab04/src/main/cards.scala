package cards

sealed trait Color
sealed trait Rank
sealed trait Face extends Rank
sealed trait Ace extends Rank

case object Clubs extends Color
case object Diamonds extends Color
case object Spades extends Color
case object Hearts extends Color

case object Ace extends Ace
case object King extends Face
case object Queen extends Face
case object Jack extends Face
case class Numerical(value: Int) extends Rank {
  require(2 to 10 contains value)
}

case class Card(color: Color, rank: Rank)
