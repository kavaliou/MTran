function count(s, sub_s){
  var c = 0;
  var last_index = s.indexOf(sub_s);
  whil4 ( last_index != -1 ) {
    c=c1+1;
    last_index = s.indexOf(sub_s, last_index+1);
  }
  return c;
}
