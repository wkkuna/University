import scala.io.Source
import scala.collection.mutable.ListBuffer
////////////// scalar ///////////////////////////
//scalar product of two vectors xs and ys
def scalarUgly(xs: List[Int], ys: List[Int]): Int = {
  var acc: Int = 0
  var i: Int = 0
  var length: Int = Math.min(xs.length, ys.length)

  while (i < length) {
    acc = acc + xs(i) * ys(i)
    i += 1
  }
  acc
}

def scalar(xs: List[Int], ys: List[Int]): Int = {
  (xs zip ys).map { case (x, y) =>
    x * y
  }.sum
}

println("Scalar")
val r = scala.util.Random
val v1 = (for (i <- 1 to 100) yield r.nextInt(100)).toList
val v2 = (for (i <- 1 to 100) yield r.nextInt(100)).toList
assert(scalar(v1, v2) == scalarUgly(v1, v2))

///////////////////////////  sort  ///////////////////////////
//quicksort algorithm
def sortUgly(xs: List[Int]): List[Int] = {
  var toSortList = xs

  def swap(i: Int, j: Int): Unit = {
    val t = toSortList(i)
    toSortList = toSortList.updated(i, toSortList(j))
    toSortList = toSortList.updated(j, t)
  }

  def sort(l: Int, r: Int): Unit = {
    val pivot = toSortList((l + r) / 2)
    var i = l
    var j = r
    while (i <= j) {
      while (toSortList(i) < pivot) i += 1
      while (toSortList(j) > pivot) j -= 1
      if (i <= j) {
        swap(i, j)
        i += 1
        j -= 1
      }
    }
    if (l < j) sort(l, j)
    if (j < r) sort(i, r)
  }

  sort(0, xs.length - 1)
  toSortList
}

def sort(xs: List[Int]): List[Int] = {
  if (xs.length <= 1) xs
  else {
    val pivot = xs(xs.length / 2)
    List.concat(
      sort(xs filter (pivot > _)),
      xs filter (pivot == _),
      sort(xs filter (pivot < _))
    )
  }
}
println("Sort")
// create a list of random ints
val randomList = (for (i <- 1 to 100) yield r.nextInt(100)).toList
val sortedPretty = sort(randomList)
val sortedUgly = sortUgly(randomList)
assert(sortedPretty == sortedUgly)

////////////////////////// isPrime ///////////////////////////
//checks if n is prime
def isPrimeUgly(n: Int): Boolean = {
  var x = 2
  while (x <= math.sqrt(n)) {
    if (n % x == 0) {
      return false
    }
    x += 1
  }
  return true
}
def isPrime(n: Int): Boolean = Range(2, n - 1).filter(n % _ == 0).length == 0

println("isPrime")
val toCheckPrimeness = (for (i <- 1 to 10) yield r.nextInt(100)).toList
val pUgly = toCheckPrimeness.map(isPrimeUgly)
val primes = toCheckPrimeness.map(isPrime)
assert(pUgly == primes)

///////////////////////// primePairs /////////////////////////
//for given positive integer n, find all pairs of integers i and j,
//where 1 ≤ j < i < n such that i + j is prime
def primePairsUgly(n: Int): List[(Int, Int)] = {
  var primePairs = ListBuffer[(Int, Int)]()
  var i = 2

  while (i < n) {
    var j = i + 1
    while (j < n) {
      if (i != j && isPrimeUgly(i + j)) {
        primePairs += ((i, j))
      }
      j += 1
    }
    i += 1
  }
  primePairs.toList
}

def primePairs(n: Int): List[(Int, Int)] = Range(2, n)
  .combinations(2)
  .map { case Seq(x, y) => (x, y) }
  .toList
  .filter(pair => isPrime(pair(0) + pair(1)))

println("primePairs")
val checkPrimePairs = r.nextInt(100)
assert(primePairsUgly(checkPrimePairs) == primePairs(checkPrimePairs))

///////////////////////// fileLines //////////////////////////
//create a list with all lines from given file
val filesHere = new java.io.File(".").listFiles
def fileLinesUgly(file: java.io.File): List[String] = {
  val f = Source.fromFile(file)
  val content = f.getLines()
  var out = ListBuffer[String]()
  while (content.hasNext) {
    val line = content.next()
    out += line
  }
  out.toList
}
def fileLines(file: java.io.File): List[String] = {
  Source.fromFile(file).getLines.toList
}
println("fileLines")
val file = filesHere(1)
assert(fileLines(file) == fileLinesUgly(file))

/////////////////////// printNonEmpty ////////////////////////
//print names of all .scala files which are in filesHere & are non
//empty
def printNonEmptyUgly(pattern: String): Unit = {
  val files_number = filesHere.length
  var i = 0
  while (i < files_number) {
    val file = filesHere(i)
    if (
      file.toString().contains(pattern) && file
        .isFile() && fileLinesUgly(file).length > 0
    ) {
      println(file.toString())
    }
    i += 1
  }
}

def printNonEmpty(pattern: String): Unit = {
  for (file <- filesHere) {
    val filename = file.toString()
    if (
      filename.contains(pattern) && file.isFile() && fileLines(file).length > 0
    ) {
      println(filename)
    }
  }
}
println("printNonEmpty")
printNonEmpty(".sc")
printNonEmptyUgly(".sc")
