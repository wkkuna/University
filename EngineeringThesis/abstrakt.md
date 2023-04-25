Tytuł: Porównanie wydajności dla różnych konfiguracji akceleratora i DMA pod wybrane płyty rozwojowe
[PL] 
Praca przeprowadza analizę porównawczą wydajności systemu złożonego z akceleratora i dwóch DMA w zależności od zastosowanej konfiguracji i płyty rozwojowej.
Konfiguracja takiego systemu składa się z magistrali do obsługi rejestrów sterowania/stanu, wspierane: AXI Lite i Wishbone, oraz magistrali odpowiedzialnych za przesył danych: AXI, Wishbone, AXI Stream. Każda z tych magistral jest konfigurowalna przynajmniej w zakresie szerokości danych i adresu.
Integrowanie powyższego systemu na wybraną płytę rozwojową jest żmudne i powtarzalne. Z tego względu użyte zostało narzędzie potrafiące ze specyfikacji połączeń sygnałów między akceleratorem a DMA wygenerować gotowy, połączony system w Verilogu, a także opis płytki rozwojowej z wygenerowanym systemem dla otwarto źródłowego generatora SoC, co pozwala na przeprowadzenie procesu syntezy i implementacji, a także wygenerowania bitstreamu.

[EN]
The work offers comparative analysis of the efficiency of the system consisting of Accelerator and two DMAs depending on configuration and chosen development board.
The system configuration consists of a control/status register bus, which could be either AXI Lite or Wishbone, as well as the data bus, where AXI, AXI Stream and Wishbone are supported. Each of these buses are configurable at least by address and data width.
Integrating this system and porting it onto the chosen development board is a gruelling, repetitive task. 
In order to generate those systems of different configurations a Accelerator Interface Generator tool was used. This tool, given the specification of signal connections between the accelerator and the DMAs, is able to generate the system in Verilog as well as a target for an open source SoC generator. This allows synthesising and implementing the design as well as generating a bitstream.