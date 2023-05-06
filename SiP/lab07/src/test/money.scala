package Tests
import Money.Money._
import Money._
object MoneyTests {
  def testAddUSDToEUR(): Unit = {
    val usd = 100.01 (USD)
    val euro = 200 (EUR)
    val total = usd + euro

    val exp = usd.amount + euro.amount * conversion((EUR, USD))
    assert(total.amount == exp)
    assert(total.currency == USD)
  }

  def testAddPLNToUSD(): Unit = {
    val zloty = 100.01 (zl)
    val dollar = 200 ($)
    val total = zloty + dollar

    val exp = zloty.amount + dollar.amount * conversion((USD, PLN))
    assert(total.amount == exp)
    assert(total.currency == PLN)
  }

  def testAddPLNToUSDWithSymbols(): Unit = {
    val zlotySymbol = 5 (zl)
    val zloty = 3 (PLN)
    val dollar = 20.5 (USD)
    val total = zlotySymbol + zloty + dollar

    val exp =
      zlotySymbol.amount + zloty.amount + dollar.amount * conversion((USD, PLN))
    assert(total.currency == PLN)
    assert(total.amount == exp)
  }

  def testSubtract(): Unit = {
    val dollar = BigDecimal(3123123123123100.01)(USD)
    val euro = 44 (EUR)
    val total = dollar - euro

    val exp = dollar.amount - euro.amount * conversion((EUR, USD))
    assert(total.currency == USD)
    assert(total.amount == exp)
  }

  def testMultiplicatePLN(): Unit = {
    val zloty = 25.8069758011 (zl)
    val multiplier = 20

    val total = zloty * multiplier

    val exp = zloty.amount * multiplier
    assert(total.currency == PLN)
    assert(total.amount == exp)
  }

  def testMultiplicateUSD(): Unit = {
    val dollar = 137 ($)
    val multiplier = 11
    val total = dollar * multiplier

    val exp = dollar.amount * multiplier
    assert(total.currency == USD)
    assert(total.amount == exp)
  }

  def testUSDToPLN(): Unit = {
    val dollar = BigDecimal(80085.01)(USD)
    val conv = dollar as PLN

    val exp = dollar.amount * conversion((USD, PLN))
    assert(conv.amount == exp)
  }

  def testUSDToEUR(): Unit = {
    val dollar = 120.01 (USD)
    val conv = dollar as `€`

    val exp = dollar.amount * conversion((USD, EUR))
    assert(conv.amount == exp)
  }

  def testCompareUSDAndEUR(): Unit = {
    assert(420.30 (USD) > 100 (`€`))
  }

  def testComparePLNAndUSD(): Unit = {
    assert(!(202.20 (USD) <= 100 (zl)))
  }

  def testCompareEURAndPLN(): Unit = {
    assert(!(2137.30 (zl) < 100 (`€`)))
  }

  def runTests(): Unit = {
    testAddUSDToEUR()
    testAddPLNToUSD()
    testAddPLNToUSDWithSymbols()

    testSubtract()

    testMultiplicatePLN()
    testMultiplicateUSD()

    testUSDToPLN()
    testUSDToEUR()

    testCompareUSDAndEUR()
    testComparePLNAndUSD()
    testCompareEURAndPLN()
  }
}
