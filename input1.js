function count(s, sub_s) 
  var c = 1;
  var last_index = s.indexOf (sub_s);
  while (last_index != -1) {
    c = c + 1;
    last_index = s.indexOf(sub_s, last_index + 1);
  }
  return c;
}
