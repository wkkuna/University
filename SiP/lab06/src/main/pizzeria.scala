package Pizzeria
trait WithPrice { val price: Double }

sealed abstract class Size(val multiplier: Double)
case object Small extends Size(0.9)
case object Regular extends Size(1)
case object Large extends Size(1.5)

sealed abstract class Crust
case object Thin extends Crust
case object Thick extends Crust

sealed abstract class Topping(val price: Double) extends WithPrice
case object Ketchup extends Topping(0.5)
case object Garlic extends Topping(0.5)

sealed abstract class Meat(val price: Double) extends WithPrice
case object Salami extends Meat(1)

sealed abstract class Drink(val price: Double) extends WithPrice
case object Lemonade extends Drink(2)

sealed abstract class Discount(val multiplier: Double)
case object Student extends Discount(0.95)
case object Senior extends Discount(0.93)
case object NoDiscount extends Discount(1)

sealed abstract class PizzaType(val price: Double) extends WithPrice
case object Margarita extends PizzaType(5)
case object Pepperoni extends PizzaType(6.5)
case object Funghi extends PizzaType(7)

case class Pizza(
    pizzaType: PizzaType,
    size: Size,
    crust: Crust,
    extraMeat: Option[Meat] = None,
    extraTopping: Option[Topping] = None
) extends WithPrice {

  override def toString: String = {
    val sep = "-"
    val separatorLen = 11
    val header = s"${sep * separatorLen}Pizza${sep * separatorLen}\n"
    val divider = s"${sep * (header.length() - 1)}\n"

    val pizzaSpec = s"""Type: $pizzaType
         |Size: $size
         |Crust: $crust
         |""".stripMargin
    val meat = extraMeat.map("Meat: " + _ + "\n").getOrElse("")
    val topping = extraTopping.map("Topping: " + _ + "\n").getOrElse("")

    header + pizzaSpec + meat + topping + divider
  }

  val extraMeatPrice: Double = extraMeat.map(_.price).sum

  val extraToppingPrice: Double = extraTopping.map(_.price).sum

  override val price: Double = {
    val coreCost = pizzaType.price
    val meatCost = extraMeatPrice
    val toppingCost = extraToppingPrice
    size.multiplier * (coreCost + meatCost + toppingCost)
  }
}
