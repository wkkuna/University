import org.scalatest.funsuite.AnyFunSuite
import componentTests._

class testDriver extends AnyFunSuite {

  test("Run basic card and deck tests") {
    DeckTests.runTests()
  }

  test("Run blackjack tests") {
    BlackjackTests.runTests()
  }
}
