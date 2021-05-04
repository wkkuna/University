# Wiktoria Kuna 316418
class Fixnum

    def czynniki
        (1...self+1).select { |elem| self%elem == 0 } 

    end 

    def ack(y)

        case 
        
        when self == 0 
            y + 1
        when y == 0
            (self-1).ack(1)
        else
            (self-1).ack(self.ack(y-1))
        end
        
    end

    def doskonala
        (1 ... self).select {|elem| self%elem == 0}.reduce(:+) == self
    end

    def slownie
        cyfry = {
            "0" => "zero",
            "1" => "jeden",
            "2" => "dwa",
            "3" => "trzy",
            "4" => "cztery",
            "5" => "pięć",
            "6" => "sześć",
            "7" => "siedem",
            "8" => "osiem",
            "9" => "dziewięć"
        }

        self.to_s().split("").map {|elem| cyfry[elem]}.join(" ")
    end

end



def main()
print 6.czynniki()
print "\n"
print 2.ack(1)
print "\n"
print 7.doskonala()
print "\n"
print 6343521.slownie() 
print "\n"
end

main()