import plugins._

import scala.annotation.tailrec

package object actions {
  // plugin applying plugins with order: SingleSpacing => Doubling => Shortening
  val actionA: Pluginable = new Pluginable
    with Shortening
    with Doubling
    with SingleSpacing

  // plugin applying plugins with order: NoSpacing => Shortening => Doubling
  val actionB: Pluginable = new Pluginable
    with Doubling
    with Shortening
    with NoSpacing

  // plugin applying plugins with order: LowerCasing => Doubling
  val actionC: Pluginable = new Pluginable with Doubling with LowerCasing

  // plugin applying plugins with order: DuplicateRemoval => Rotating
  val actionD: Pluginable = new Pluginable with Rotating with DuplicateRemoval

  // plugin applying plugins with order: NoSpacing => Shortening => Doubling => Reverting
  val actionE: Pluginable = new Pluginable
    with Reverting
    with Doubling
    with Shortening
    with NoSpacing

  // plugin applying plugin Rotating 5-times
  val actionF: Pluginable = new Pluginable with Rotating {
    override def plugin(s: String): String =
      Iterator.iterate(s)(super.plugin).drop(5).next()
  }

  // plugin applying plugins with order: actionA => actionB
  val actionG: Pluginable = new Pluginable {
    override def plugin(s: String): String = actionB.plugin(actionA.plugin(s))
  }
}
