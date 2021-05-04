# Wiktoria Kuna 316418

class Kolekcja
    def initialize
        @kolekcja = []
        @length = 0
    end

    def swap(i, j)
        x = @kolekcja[i]
        @kolekcja[i] = @kolekcja[j]
        @kolekcja[j] = x
    end

    def length
        @length
    end

    def get(i)
        @kolekcja[i]
    end

    def put(elem)
        @kolekcja[@length] = elem
        @length += 1
    end

    def putlist(x)
        x.each do |i|
            put(i)
        end
    end

    def delete(idx)
        @kolekcja.delete_at(idx)
    end
end

class Sortowanie

    def sort1(kolekcja)
        n = kolekcja.length
        swapped = true
        while swapped
            
            swapped = false

            (n - 1).times do |i|
                if kolekcja.get(i) > kolekcja.get(i+1) 
                   kolekcja.swap(i, i+1)
                   swapped = true
                end
            end
        end
    end

    def sort2(kolekcja)
        n = kolekcja.length
        (n - 1).times do |j|
          while j > 0
            if kolekcja.get(j-1) > kolekcja.get(j)
              kolekcja.swap(j, j-1)
            else
              break
            end
            j -= 1
          end
        end
      end
end

def Main()
    a = Kolekcja.new() 
    b = Kolekcja.new()
    a.putlist([1, 9, -1, 111, 69])
    a.put(-3)
    a.put(123)

    b.putlist([231, 3123, -23, 323, -3123, -756, 1943, 0])
    g = Sortowanie.new()
    g.sort2(a)
    g.sort1(b)

    print "Kolekcja a:\n"
    [0 ... a.length].each do |e|
        puts a.get(e)
    end 
    print "\n"

    print "Kolekcja b:\n"
    [0 ... b.length].each do |e|
        puts b.get(e)
    end 
end

Main()