package Tests
import Pizzeria._
import Orders._

object OrdersTests {
  def testInvalidPhoneNumber(): Unit = {
    try {
      // Don't want no british to get pizza
      val _ = new Order(
        "Alice",
        "God Save the Queen",
        "020 7946 0750",
        Some(List(Pizza(Margarita, Regular, Thick))),
        Some(List(Lemonade))
      )
    } catch {
      case _: IllegalArgumentException => ()
      case _: Throwable =>
        assert(assertion = false, "Failed when given invalid phone number")
    }
  }

  def testExtraMeat(): Unit = {
    val pizza = Pizza(Margarita, Regular, Thick, Some(Salami))
    val pizza2 = Pizza(Pepperoni, Regular, Thin, Some(Salami))
    val order = new Order(
      "john",
      "some street 7",
      "123456789",
      Some(List(pizza, pizza2)),
      Some(List(Lemonade))
    )

    val extraMeatPrice = order.extraMeatPrice

    assert(extraMeatPrice.get == pizza.extraMeatPrice + pizza2.extraMeatPrice)
  }

  def testTwoPizzaOrder(): Unit = {
    val pizza = Pizza(Margarita, Regular, Thin, Some(Salami))
    val pizza2 = Pizza(Pepperoni, Regular, Thick, Some(Salami))
    val order = new Order(
      "Emei",
      "Frying Pan Road 9",
      "123456789",
      Some(List(pizza, pizza2)),
      Some(List(Lemonade))
    )

    val price = order.totalPizzaPrice

    assert(price.get == pizza.price + pizza2.price)
  }

  def testPizzaType(): Unit = {
    val pizza = Pizza(Margarita, Regular, Thin, Some(Salami))
    val pizza2 = Pizza(Pepperoni, Regular, Thick, Some(Salami))
    val order = new Order(
      "Emei",
      "Frying Pan Road 9",
      "123456789",
      Some(List(pizza, pizza2)),
      Some(List(Lemonade))
    )

    val price = order.priceByType(Margarita)

    assert(price.get == pizza.price)
  }

  def testTotalPrice(): Unit = {
    val pizza = Pizza(Margarita, Regular, Thick, Some(Salami))
    val order = new Order(
      "Emei",
      "Frying Pan Road 9",
      "123456789",
      Some(List(pizza)),
      Some(List(Lemonade))
    )

    val price = order.price

    assert(price == pizza.price + Lemonade.price)
  }

  def testDiscount(): Unit = {
    val pizzas = List(Pizza(Margarita, Regular, Thick, Some(Salami)))
    val drinks = List(Lemonade)

    val orderNoDiscount = new Order(
      "Emei",
      "Frying Pan Road 9",
      "123456789",
      Some(pizzas),
      Some(drinks)
    )

    val orderDiscount = new Order(
      "Emei",
      "Frying Pan Road 9",
      "123456789",
      Some(pizzas),
      Some(drinks),
      Some(Senior)
    )

    assert(orderNoDiscount.price * 0.93 == orderDiscount.price)
  }

  def testPrintOrder(): Unit = {
    val pizza = Pizza(Margarita, Regular, Thick, Some(Salami))
    val pizza2 = Pizza(Pepperoni, Regular, Thick, Some(Salami))
    val order = new Order(
      "Emei",
      "Frying Pan Road 9",
      "123456789",
      Some(List(pizza, pizza2)),
      Some(List(Lemonade)),
      specialInfo=Some("Please don't ring my cats are attacking the door\n")
    )

    print(order)
  }

  def runTests(): Unit = {
    testInvalidPhoneNumber()
    testExtraMeat()
    testTwoPizzaOrder()
    testPizzaType()
    testTotalPrice()
    testDiscount()
    testPrintOrder()
  }

}
