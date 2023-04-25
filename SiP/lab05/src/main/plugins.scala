package object plugins {

  trait Pluginable {
    def plugin(s: String): String = s
  }

  trait Reverting extends Pluginable {
    override def plugin(s: String): String = super.plugin(s.reverse)
  }

  trait LowerCasing extends Pluginable {
    override def plugin(s: String): String = super.plugin(s.toLowerCase)
  }

  trait SingleSpacing extends Pluginable {
    override def plugin(s: String): String =
      super.plugin(s.replaceAll(" +", " "))
  }

  trait NoSpacing extends Pluginable {
    override def plugin(s: String): String =
      super.plugin(s.replaceAll(" +", ""))
  }

  trait DuplicateRemoval extends Pluginable {
    override def plugin(s: String): String = {
      val occurences =
        s.groupBy(identity).view.mapValues(_.map(_ => 1).reduce(_ + _))
      super.plugin(s filter (occurences(_) == 1))
    }
  }

  trait Rotating extends Pluginable {
    override def plugin(s: String): String = super.plugin(s"${s.last}${s.init}")
  }

  trait Doubling extends Pluginable {
    override def plugin(s: String): String =
      super.plugin(
        s.zipWithIndex
          .map({ case (v: Char, k: Int) => if (k % 2 == 1) s"$v$v" else v })
          .mkString
      )
  }

  trait Shortening extends Pluginable {
    override def plugin(s: String): String =
      super.plugin(
        s.zipWithIndex
          .map({ case (v: Char, k: Int) => if (k % 2 == 0) v else "" })
          .mkString
      )
  }
}
