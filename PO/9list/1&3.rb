# Wiktoria Kuna 316418

class Funkcja

    @fun
    @epsilon
    def initialize(function)
       @fun = function
       @epsilon = 10e-5
       @rd_val = 5
    end

    def value(x)
        @fun.(x).round(@rd_val)
    end

    def root(a,b,e)
        rd = Math.log10((1/e)) + 1
        puts rd
        
        rt = a.step(b, e).to_a.select{|x| @fun.(x).abs < e }.map{|x| x.round(rd)}

        rt.empty?? nil : rt
    end

    def area(a,b) 
        a.step(b, @epsilon).to_a{}.reduce(0) {|s,x| s + @fun.(x).abs()*@epsilon}.round(@rd_val)
    end

    def deriv(x)
        ((@fun.(x+@epsilon) - @fun.(x))/@epsilon).round(@rd_val)
    end

    def draw(a, b)

        approx = ((b - a)/1000.0).abs

        File.open("data.txt", 'w') do |file| 
            a.step(b,approx).each{|x| file.puts(x.to_s+","+self.value(x).to_s)}
        end 

        sleep(0.01)
        File.open("fun.gnuplot", 'w') do |file|
            file.puts(
                " set datafile separator ',' \n
                set xrange [#{a}:#{b}]
                set zeroaxis linetype 8
                set title \"Inputed function\" \n
                plot \"data.txt\" using 1:2 with lines title \'fun\'"
            )
        end
         
         system("gnuplot -p fun.gnuplot")
         system("rm data.txt")
         system("rm fun.gnuplot")
    end
end


def Main()
    a = Funkcja.new(Proc.new{|x| x*(x-2.32)})
     puts a.value(2)
     print a.root(-10, 10, 10e-5)
     puts "\n"
     puts a.area(-8, 2)
     puts a.deriv(1)
     puts a.value(3.14159)
     a.draw(-8,8)
end 

Main()
