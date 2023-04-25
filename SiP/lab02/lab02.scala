import scala.math
import java.awt.Point
import org.w3c.dom.css.Rect

package numbers {

  class Rational(numerator: Int, denumerator: Int) {
    require(denumerator != 0, "Division by 0 is illegal!")
    private def gcd(a: Int, b: Int): Int = if (b == 0) a else gcd(b, a % b)
    private def lcm(a: Int, b: Int): Int = (a * b) / gcd(a.abs, b.abs)
    private val gcdVal = gcd(numerator, denumerator).abs
    val p = numerator / gcdVal
    val q = denumerator / gcdVal

    // addition
    def +(other: Rational): Rational = {
      val qq_lcm = lcm(q.abs, other.q.abs)
      val new_p = p * (qq_lcm / q) + other.p * (qq_lcm / other.q)
      val new_q = qq_lcm
      Rational(new_p, new_q)
    }
    // subtraction
    def -(other: Rational): Rational = {
      Rational(p, q) + Rational(-other.p, other.q)
    }
    // multiplication
    def *(other: Rational): Rational = {
      val new_p = p * other.p
      val new_q = q * other.q
      Rational(new_p, new_q)
    }
    // division
    def /(other: Rational): Rational =
      Rational(p, q) * Rational(other.q, other.p)

    def toDouble: Double = p / q
    def sqrt: Double = math.sqrt(toDouble)

    override def toString: String = {
      p match {
        case 0 => "0"
        case x if x < q => s"$x/$q"
        case x if x % q == 0 => s"${x / q}"
        case x => s"${x / q} ${x % q}/$q"
      }
    }
  }

  object Rational {
    val zero: Rational = Rational(0, 1)
    val one: Rational = Rational(1, 1)
    def apply(p: Int, q: Int = 1) = new Rational(p, q)
  }
}

package figures {

  import numbers.Rational
  class Point(x: Rational, y: Rational) {
    def coordX = x
    def coordY = y

    def this(x: Int, y: Int) = this(Rational(x), Rational(y))

    def euclidianDistance(v: Point): Double = {
      ((x - v.coordX) * (x - v.coordX) + (y - v.coordY) * (y - v.coordY)).sqrt
    }
    override def toString(): String = s"($x, $y)"
  }

  abstract class Figure {
    def area: Double
    val description: String
  }

  class Triangle(x: Point, y: Point, z: Point) extends Figure {
    val edges =
      List(
        x.euclidianDistance(y),
        x.euclidianDistance(z),
        z.euclidianDistance(y)
      )
    def area: Double = {
      val s = edges.sum / 2
      math.sqrt(s * (s - edges(0)) * (s - edges(1)) * (s - edges(2)))

    }
    val description: String = "Triangle"
  }

  class Rectangle(x: Point, y: Point, z: Point, w: Point) extends Figure {
    val edges =
      List(
        x.euclidianDistance(y),
        y.euclidianDistance(z),
        z.euclidianDistance(w),
        w.euclidianDistance(x)
      )
    def area: Double = edges(0) * edges(1)
    val description: String = "Rectangle"
  }
  class Square(x: Point, y: Point, z: Point, w: Point) extends Rectangle {
    val description: String = "Square"
  }

}

package singleton {
  object FiguresUtil {
    import figures.Figure
    def areaSum(figures: List[Figure]): Double =
      figures.map(x => x.area).sum // Sum all areas
    def printAll(figures: List[Figure]): Unit = for (x <- figures)
      print(s"${x.description} ") // Print all descriptions
  }
}

object App {
  def main(args: Array[String]): Unit = {
    // The number visual part
    import numbers.Rational
    import figures._

    val x = Rational(3, 6)
    val y = Rational(9, 60)
    println(s"X: ${x}, Y: ${y}")
    println(s"X + Y = ${x + y}")
    println(s"Y - X = ${y - x}")
    println(s"X * Y = ${x * y}")
    println(s"X / Y = ${x / y}")

    // Figures visuals
    val p0 = new figures.Point(Rational.zero, Rational.zero)
    val p1 = new figures.Point(1, 2)
    val p2 = new figures.Point(3, 2)
    println(p0)

    val t = new Triangle(p0, p1, p2)

    val p11 = new figures.Point(1, 1)
    val p10 = new figures.Point(1, 0)
    val p01 = new figures.Point(0, 1)

    val rec = new figures.Rectangle(p0, p01, p10, p11)
    val sq = new figures.Square(p0, p01, p10, p11)
    import singleton.FiguresUtil._
    val figs = List(t, rec, sq)
    printAll(figs)
    println(areaSum(figs))
  }
}
