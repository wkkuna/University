package Tests
import Pizzeria._

object PizzeriaTests {
  def runTests(): Unit = {
    val pizzaWithoutOptionals = Pizza(Margarita, Regular, Thick)
    val pizzaWithOptionals =
      Pizza(Margarita, Regular, Thick, Some(Salami), Some(Ketchup))

    assert(pizzaWithOptionals.price > pizzaWithoutOptionals.price)
  }
}
