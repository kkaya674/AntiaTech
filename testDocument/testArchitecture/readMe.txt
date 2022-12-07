Test Types: 
	Unit Test : 
		Component bazlı yaptığımız testler. Örneğin bir ekipmanın çalışıp çalışmadığını, çalıştığı durumda ne gibi bir behaviour gösterdiğini anlatan testtir. 

	Feature Test:
		Componentlerin bir araya gelerek olusturduğu en kücük birim. Sub-sistemlerin çalışırlığı bir Feature test olarak görülebilir. 
		Örneğin top fırlatma mekanizmasını test etmek. 
	Integration Test:
		Farklı componentleri birleştirdiğimiz zaman sistemin nasıl davrandığını izleyen testtir.
		Kıyaslama yapacak olursak dc motoru dc supply'dan gelen voltaja görerek sürdüğümüz test bir feature test iken,
		İkincil bir cihazdan, örneğin raspberry'den ya da  ikinci bir arduino'dan gelen komutla bu topu fırlatmaya çalışmak bir integration testtir. 

	Acceptance Test:
		Bitmiş projenin tümünü test eden senaryodur. Demo'dan önce 1 defa yapmamız gerekir. Aslında burada masa tenisi oynarken hayal ettiğimiz senaryolar geçerlidir. 
