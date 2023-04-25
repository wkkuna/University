import plugins._

package object PluginTests {

  def testRevertNonEmpty(): Unit = {
    val plugin = new Pluginable with Reverting
    assert(plugin.plugin("; crabs") == "sbarc ;")
  }

  def testRevertEmpty(): Unit = {
    val plugin = new Pluginable with Reverting
    assert(plugin.plugin("") == "")
  }

  def testLowerCase(): Unit = {
    val plugin = new Pluginable with LowerCasing
    val out = plugin.plugin("DuCkS Are so COOL I WaNnA hug thEM")
    assert(out == "ducks are so cool i wanna hug them")
  }

  def testChainLowerCaseAndReverse(): Unit = {
    val plugin = new Pluginable with Reverting with LowerCasing
    val s =
      "Raccoons  look like  lvl50 thievEs, but I could    watCh them  eat grApes all day."
    val out = plugin.plugin(s)
    assert(
      out == ".yad lla separg tae  meht hctaw    dluoc i tub ,seveiht 05lvl  ekil kool  snooccar"
    )
  }

  def testSingleSpacing(): Unit = {
    val plugin = new Pluginable with SingleSpacing
    assert(plugin.plugin("Fluff  -   ball   !   ") == "Fluff - ball ! ")
  }

  def testNoSpacing(): Unit = {
    val plugin = new Pluginable with NoSpacing
    assert(plugin.plugin("Fluff  -   ball   !   ") == "Fluff-ball!")
  }

  def testRemoveDuplicates(): Unit = {
    val plugin = new Pluginable with DuplicateRemoval
    assert(plugin.plugin("a a bba c d f  a g h s") == "cdfghs")
  }

  def testRotateOnce(): Unit = {
    val plugin = new Pluginable with Rotating
    assert(plugin.plugin("rawr") == "rraw")
  }

  def testDoubling(): Unit = {
    val plugin = new Pluginable with Doubling
    val out = plugin.plugin("acab")
    assert(out == "accabb")
  }

  def testShortening(): Unit = {
    val plugin = new Pluginable with Shortening
    assert(plugin.plugin("baubncndye") == "bunny")
  }

  def runTests(): Unit = {
    testRevertNonEmpty()
    testRevertEmpty()

    testLowerCase()

    testSingleSpacing()

    testNoSpacing()

    testRemoveDuplicates()

    testRotateOnce()

    testDoubling()

    testShortening()

    testChainLowerCaseAndReverse()
  }
}
