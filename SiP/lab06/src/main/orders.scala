package Orders
import Pizzeria._

  class Order(
      name: String,
      address: String,
      phone: String,
      pizzas: Option[List[Pizza]],
      drinks: Option[List[Drink]],
      discount: Option[Discount] = None,
      specialInfo: Option[String] = None
  ) {

    // Assume polish numbers with no area code
    require(phone.matches("[0-9]{9}"))
    private val sep = "-"
    private val sepLen = 11
    private val headerWidth = 80

    override def toString: String = {
      def getHeader(title: String): String =
        s"${sep * sepLen}${title}${sep * sepLen}\n"
      val orderHeader = getHeader("Order")
      val divider = s"${sep * (orderHeader.length() - 1)}\n"
      val deliveryAddress = "Delivery Address:\n" + divider +
        s"""|Name: $name
           |Address: $address
           |Phone $phone
           |""".stripMargin + divider

      val pizzzaInfo = pizzas match {
        case Some(values) =>
          "Pizzas:\n" + divider + values.map(_.toString).mkString("")
        case None => ""
      }
      val drinksInfo = drinks match {
        case Some(values) =>
          "Drinks:\n" + divider + values.map(_.toString).mkString(", ") + "\n"
        case None => ""
      }
      val discountInfo =
        discount.map("Discount: " + _.toString + "\n").getOrElse("")
      val extraInfo = specialInfo.map("Extra Info: " + _).getOrElse("")

      orderHeader + deliveryAddress + pizzzaInfo + drinksInfo + discountInfo + extraInfo + divider
    }

    def extraMeatPrice: Option[Double] = pizzas.map(_.map(_.extraMeatPrice).sum)

    def totalPizzaPrice: Option[Double] = pizzas.map(_.map(_.price).sum)

    def totalDrinkPrice: Option[Double] = drinks.map(_.map(_.price).sum)

    def priceByType(pizzaType: PizzaType): Option[Double] = pizzas
      .map(
        _.filter(_.pizzaType == pizzaType)
          .map(_.price)
          .sum
      )

    val price: Double = {
      val discountMultiplier = discount.getOrElse(NoDiscount).multiplier

      val priceOfPizzas: Double = totalPizzaPrice.getOrElse(0)
      val priceOfDrinks: Double = totalDrinkPrice.getOrElse(0)

      discountMultiplier * (priceOfPizzas + priceOfDrinks)
    }
  }

