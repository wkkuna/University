import actions._

package object ActionTests {
  def testActionA(): Unit = {
    val in = "b   s s sdasdas  a"
    val exp = "b  s dasas "
    assert(actionA.plugin(in) == exp)
  }

  def testActionB(): Unit = {
    val in = "um fermentum. Aliquam finibus eleifend"
    val exp = "uffreetmmAiiummiiiueeeffn"
    assert(actionB.plugin(in) == exp)
  }

  def testActionC(): Unit = {
    val in = "Curabitur ut tellus ultricies, vulputate orci nec,"
    val exp =
      "cuuraabiituur  utt ttellluus  ulltrricciees,, vvullpuutaatee oorcci  neec,,"
    assert(actionC.plugin(in) == exp)
  }

  def testActionD(): Unit = {
    val in = "condimentum por"
    val exp = "rcdietu p"
    assert(actionD.plugin(in) == exp)
  }

  def testActionE(): Unit = {
    val in = "Lorem ipsum dolor sit amet, "
    val exp = ",,eaairrldduppmrrL"
    assert(actionE.plugin(in) == exp)
  }

  def testActionF(): Unit = {
    val in = "abcdef"
    val exp = "bcdefa"
    assert(actionF.plugin(in) == exp)
  }

  def testActionG(): Unit = {
    val in = "Assume that your code"
    val exp = "Auuehhyrrd"
    assert(actionG.plugin(in) == exp)
  }

  def runTests(): Unit = {
    testActionA()
    testActionB()
    testActionC()
    testActionD()
    testActionE()
    testActionF()
    testActionG()
  }
}
