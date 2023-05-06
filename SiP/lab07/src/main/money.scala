package Money

import scala.language.implicitConversions
import play.api.libs.json._

sealed trait Currency extends Product {
  // So that currency <code> is printed as <code>
  override def toString(): String = this.productPrefix
}

case object USD extends Currency
case object EUR extends Currency
case object PLN extends Currency

sealed abstract class CurrencySymbol(val currency: Currency)
case object $ extends CurrencySymbol(USD)
case object `€` extends CurrencySymbol(EUR)
case object zl extends CurrencySymbol(PLN)

case class CurrencyConverter(
    conversion: Map[(Currency, Currency), BigDecimal]
) {
  def convert(from: Currency, to: Currency): BigDecimal =
    conversion((from, to))

  def convert(from: CurrencySymbol, to: CurrencySymbol): BigDecimal =
    conversion((from.currency, to.currency))
}

case class Money(amount: BigDecimal, currency: Currency)(implicit
    currencyConverter: CurrencyConverter
) {
  def as(other: Currency): Money =
    Money(amount * currencyConverter.convert(currency, other), other)

  def +(other: Money): Money =
    Money(amount + (other as currency).amount, currency)

  def -(other: Money): Money =
    Money(amount - (other as currency).amount, currency)

  def *(multiplier: Double): Money = Money(amount * multiplier, currency)

  def >(other: Money): Boolean = amount > (other as currency).amount

  def <(other: Money): Boolean = amount < (other as currency).amount

  def ==(other: Money): Boolean = amount == (other as currency).amount

  def !=(other: Money): Boolean = ! ==(other)

  def >=(other: Money): Boolean = ! <(other)

  def <=(other: Money): Boolean = ! >(other)
}

object Money {
  // Fetch the exchange rates from exchangerate.host API
  private def getExchangeRates(
      code: Currency,
      codes: List[Currency]
  ): JsValue = Json.parse(
    scala.io.Source
      .fromURL(
        s"https://api.exchangerate.host/latest?base=${code}&symbols=${codes.mkString(",")}"
      )
      .getLines()
      .mkString
  )

  private def getConversionMap(
      codes: List[Currency]
  ): Map[(Currency, Currency), BigDecimal] =
    (for (baseCode <- codes) yield {
      val rate = getExchangeRates(baseCode, codes)
      for (c <- codes)
        yield (
          (baseCode, c),
          (rate \ "rates" \ c.toString()).get.as[BigDecimal]
        )
    }).flatten.toMap

  val conversion: Map[(Currency, Currency), BigDecimal] =
    getConversionMap(List(USD, PLN, EUR))

  implicit def symbolToCurrency(symbol: CurrencySymbol): Currency =
    symbol.currency

  implicit def bigDecimalToMoney(amount: BigDecimal): Currency => Money =
    (currency: Currency) =>
      Money(amount, currency)(CurrencyConverter(conversion))

  implicit def doubleToMoney(amount: Double): Currency => Money =
    (currency: Currency) =>
      Money(amount, currency)(CurrencyConverter(conversion))
}
