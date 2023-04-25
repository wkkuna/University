scalaVersion := "2.13.8"

name := "Options"

Compile / scalaSource := baseDirectory.value / "src" / "main"
Test / scalaSource := baseDirectory.value / "src" / "test"

libraryDependencies ++= Seq("org.scalatest" %% "scalatest" % "3.2.15" % "test")
scalacOptions ++= Seq("-deprecation")
