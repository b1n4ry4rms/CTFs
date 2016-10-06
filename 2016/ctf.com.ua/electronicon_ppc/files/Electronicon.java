package ua.com.ctf;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.HashMap;
import java.util.HashSet;
import org.bouncycastle.util.encoders.Hex;

public class Electronicon {

	static final int code0 = -909752615;
	static final int code1 = -2107102939;
	static final int code2 = 704684177;
	static final int code3 = 1055724713;
	static final int code4 = 1743160341;
	static final int code5 = -1990087535;
	static final int code6 = 1569275284;
	static final int code7 = -2008324671;
	static final int code8 = 1609697413;
	static final int code9 = -1321152052;
	static final int codeA = -1103728844;
	static final int codeB = 664754984;
	static final int codeC = 960108517;
	static final int codeD = -759676910;
	static final int codeE = 1457260857;
	static final int codeF = -550691455;

	public static void main(String[] args) {
		HashMap<Integer, Character> hm = new HashMap<>();
		hm.put(code1, '1');
		hm.put(code2, '2');
		hm.put(code3, '3');
		hm.put(code4, '4');
		hm.put(code5, '5');
		hm.put(code6, '6');
		hm.put(code7, '7');
		hm.put(code8, '8');
		hm.put(code9, '9');
		hm.put(code0, '0');
		hm.put(codeA, 'a');
		hm.put(codeB, 'b');
		hm.put(codeC, 'c');
		hm.put(codeD, 'd');
		hm.put(codeE, 'e');
		hm.put(codeF, 'f');

		try {
			byte[] b = Files.readAllBytes(Paths.get("/tmp/ctf/h4ck1t/pain.txt"));
			String s = new String(b);
			String sa[] = s.split(String.valueOf((char) 0x0A));
			HashSet<String> ts = new HashSet<>();
			int z = new String(sa[0]).length() / 13, y = 0;
			StringBuilder h = new StringBuilder();
			for (int i = 0; i < z; i++) {
				StringBuilder sb = new StringBuilder();
				for (String string : sa) {
					String w = string.substring(y, y + 13);
					sb.append(w);
				}
				ts.add(sb.toString());
				h.append(hm.get(sb.toString().hashCode()));
				y = y + 13;
			}
			System.out.println(h);
			Files.write(Paths.get("/tmp/ctf/h4ck1t/electronicon.jpg"), Hex.decode(h.toString()), StandardOpenOption.CREATE);
			System.out.println(ts.size());
			for (String string : ts) {
				y = 0;
				for (int i = 0; i < sa.length; i++) {
					String ss = string.substring(y, y + 13);
					y = y + 13;
					System.out.println(ss);
				}
				System.out.println(string.hashCode());
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}