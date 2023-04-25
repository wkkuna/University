import org.scalatest.funsuite.AnyFunSuite
import PluginTests._
import ActionTests._

class testDriver extends AnyFunSuite {

  test("Run basic plugin text manipulation tests") {
    PluginTests.runTests()
  }
  test("Run actions tests") {
    ActionTests.runTests()
  }
}
