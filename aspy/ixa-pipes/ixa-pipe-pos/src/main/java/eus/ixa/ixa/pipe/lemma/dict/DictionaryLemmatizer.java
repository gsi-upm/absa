/*
 * Copyright 2014 Rodrigo Agerri

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
 */

package eus.ixa.ixa.pipe.lemma.dict;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import eus.ixa.ixa.pipe.lemma.Lemmatizer;

/**
 * Lemmatize by simple dictionary lookup into a hashmap built from a file
 * containing, for each line, word\tablemma\tabpostag.
 * 
 * @author ragerri
 * @version 2014-07-08
 */
public class DictionaryLemmatizer implements Lemmatizer {

  /**
   * The hashmap containing the dictionary.
   */
  private final HashMap<List<String>, String> dictMap;

  /**
   * Construct a hashmap from the input tab separated dictionary.
   * 
   * The input file should have, for each line, word\tablemma\tabpostag
   * 
   * @param dictionary
   *          the input dictionary via inputstream
   */
  public DictionaryLemmatizer(final InputStream dictionary) {
    this.dictMap = new HashMap<List<String>, String>();
    final BufferedReader breader = new BufferedReader(new InputStreamReader(
        dictionary));
    String line;
    try {
      while ((line = breader.readLine()) != null) {
        final String[] elems = line.split("\t");
        this.dictMap.put(Arrays.asList(elems[0], elems[2]), elems[1]);
      }
    } catch (final IOException e) {
      e.printStackTrace();
    }
  }

  /**
   * Get the Map containing the dictionary.
   * 
   * @return dictMap the Map
   */
  public HashMap<List<String>, String> getDictMap() {
    return this.dictMap;
  }

  /**
   * Get the dictionary keys (word and postag).
   * 
   * @param word
   *          the surface form word
   * @param postag
   *          the assigned postag
   * @return returns the dictionary keys
   */
  private List<String> getDictKeys(final String word, final String postag) {
    final List<String> keys = new ArrayList<String>();
    keys.addAll(Arrays.asList(word.toLowerCase(), postag));
    return keys;
  }
  
  /* (non-Javadoc)
   * @see eus.ixa.ixa.pipe.lemma.Lemmatizer#lemmatize(java.lang.String[], java.lang.String[])
   */
  public String[] lemmatize(final String[] tokens, final String[] postags) {
    List<String> lemmas = new ArrayList<String>();
    for (int i = 0; i < tokens.length; i++) {
      lemmas.add(this.apply(tokens[i], postags[i])); 
    }
    return lemmas.toArray(new String[lemmas.size()]);
  }

  /**
   * Lookup lemma in a dictionary. Outputs "O" if not found.
   * @param word the token
   * @param postag the postag
   * @return the lemma
   */
  public String apply(final String word, final String postag) {
    String lemma = null;
    final List<String> keys = this.getDictKeys(word, postag);
    // lookup lemma as value of the map
    final String keyValue = this.dictMap.get(keys);
    if (keyValue != null) {
      lemma = keyValue;
    } else {
      lemma = "O";
    }
    return lemma;
  }
}
