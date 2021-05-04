# Wiktoria Kuna 316418
class Jawny

    def initialize(str)
        @jawny = str            
    end
    
    def zaszyfruj(klucz)
        Zaszyfrowany.new (@jawny.split("").map {|elem| klucz[elem]}.join)
    end

    def to_s
        @jawny
    end
end  


class Zaszyfrowany

    def initialize(str)
        @zaszyfrowany = str            
    end
    
    def odszyfruj(klucz)
        Jawny.new (@zaszyfrowany.split("").map {|elem| klucz[elem]}.join)
    end

    def to_s
        @zaszyfrowany
    end
end

def main
    slownik = {
        "a" => "z",
        "b" => "y",
        "c" => "x",
        "d" => "w",
        "e" => "v",
        "f" => "u",
        "g" => "t",
        "h" => "s",
        "i" => "r",
        "j" => "q",
        "k" => "p",
        "l" => "o",
        "m" => "n",
        "n" => "m",
        "o" => "l",
        "p" => "k",
        "q" => "j",
        "r" => "i",
        "s" => "h",
        "t" => "g",
        "u" => "f",
        "v" => "e",
        "w" => "d",
        "x" => "c",
        "y" => "b",
        "z" => "a"
    }
   slownik2 = Hash.new
   slownik.each {|k,v| slownik2[v] = k}

    x = Jawny.new("uwu")
    print x.to_s
    print "\n"
    print x.zaszyfruj(slownik).to_s
    print "\n"
    print x.zaszyfruj(slownik).odszyfruj(slownik2).to_s
    print "\n"
end


main()