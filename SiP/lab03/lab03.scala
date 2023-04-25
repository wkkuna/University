object Utils {
  def isSorted(as: List[Int], ordering: (Int, Int) => Boolean): Boolean =
    as match {
      case List() => true
      case List(_) => true
      case _ =>
        as.grouped(2).forall {
          case List(x, y) => ordering(x, y)
          case _ => true
        }
    }
  def isAscSorted(as: List[Int]) = isSorted(as, (x: Int, y: Int) => x < y)
  def isDescSorted(as: List[Int]) = isSorted(as, (x: Int, y: Int) => x > y)
  def foldLeft[A, B](l: List[A], z: B)(f: (B, A) => B): B = {
    l match {
      case Nil => z
      case x :: xs => foldLeft(xs, f(z, x))(f)
    }
  }
  def sum(l: List[Int]): Int = foldLeft(l, 0)((x, y) => x + y)
  def length[A](l: List[A]): Int = foldLeft(l, 0)((x, y) => x + 1)
  def compose[A, B, C](f: B => C, g: A => B) = { x: A =>
    f(g(x))
  }
  def repeated[A](f: A => A, n: Int): A => A = {
    {
      if (n == 0) {
        identity
      } else {
        compose(repeated(f, n - 1), f)
      }

    }
  }
  def curry[A, B, C](f: (A, B) => C) = (x: A) => (y: B) => f(x, y)
  def uncurry[A, B, C](f: (A => B => C)): (A, B) => C = (x: A, y: B) => f(x)(y)

  
  def unSafe[T](ex: Exception)(block: => T): T = {
    try {
      block
    } catch {
      case error: Throwable =>
        println(s"logging error: ${error.getMessage}")
        throw ex
    }
  }
}
object UnsafeTest {
  import Utils.unSafe
  class ExampleException extends Exception

  def run(): Unit = {
    try {
      unSafe(new ExampleException()) {
        generateError()
      }
    } catch {
      case _: ExampleException => ()
      case err: Throwable => println(s"invalid error, got ${err.getMessage}")
    }
  }

  def generateError(): Int = {
    1 / 0
  }
}

object App {
  def main(args: Array[String]): Unit = {
    import Utils._
    val xs = List(1, 2, 3, 4)
    println(s"Tests for list: ${xs}")
    println(
      s"Is xs sorted with ordering < ? ${isSorted(xs, (x: Int, y: Int) => x < y)}"
    )
    println(
      s"Is xs sorted with ordering > ? ${isSorted(xs, (x: Int, y: Int) => x > y)}"
    )
    println(
      s"Is xs sorted ascending? ${isSorted(xs, (x: Int, y: Int) => x < y)}"
    )
    println(
      s"Is xs sorted descending? ${isSorted(xs, (x: Int, y: Int) => x > y)}"
    )
    println(s"Sum of xs ${sum(xs)}")
    println(s"Length of xs ${length(xs)}")
    val f: Int => Int = (x) => x + 1
    val x = 5
    println(
      s"Do the repeat of f(x) = x + 1, let's say 6 times, result from x=${x} ${repeated(f, 6)(x)}"
    )
    val add = (x: Int, y: Int) => x + y
    println(
      s"Curry example: curry(add)(4)(2): ${curry(add)(4)(2)} and add(4, 2)s: ${4 + 2}"
    )
    println(
      s"Uncurry example for uncurry previous function: ${uncurry(curry(add))(4, 2)} and add(4)(2) ${4 + 2}"
    )
    import UnsafeTest.run
    run()
  }
}
