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
package eus.ixa.ixa.pipe.nerc.features;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import opennlp.tools.util.InvalidFormatException;
import opennlp.tools.util.featuregen.CustomFeatureGenerator;
import opennlp.tools.util.featuregen.FeatureGeneratorResourceProvider;

public class Prev2MapFeatureGenerator extends CustomFeatureGenerator {
  
  private Map<String, String> previousMap = new HashMap<String, String>();

  public void createFeatures(List<String> features, String[] tokens, int index, String[] preds) {
    
    if (index > 0) {
      features.add("ppd=" + previousMap.get(tokens[index]) + "," + previousMap.get(tokens[index - 1]));
    }
  }

  /**
   * Generates previous decision features for the token based on contents of the previous map.
   */
  public void updateAdaptiveData(String[] tokens, String[] outcomes) {

    for (int i = 0; i < tokens.length; i++) {
      previousMap.put(tokens[i], outcomes[i]);
    }
  }

  /**
   * Clears the previous map.
   */
  public void clearAdaptiveData() {
    previousMap.clear();
  }

  @Override
  public void init(Map<String, String> properties,
      FeatureGeneratorResourceProvider resourceProvider)
      throws InvalidFormatException {
    
  }

}
