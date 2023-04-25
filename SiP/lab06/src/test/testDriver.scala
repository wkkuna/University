package Tests
import org.scalatest.funsuite.AnyFunSuite

class testDriver extends AnyFunSuite {

  test("Run pizzeria test") {
    PizzeriaTests.runTests()
  }
  test("Run orders test") {
    OrdersTests.runTests()
  }
}
