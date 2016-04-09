# -*- coding: utf-8 -*-
"""
Mining Assignment 1
"""

import math

#################################################
# recommender class does user-based filtering and recommends items 
class UserBasedFilteringRecommender:
    
    # class variables:    
    # none
    
    ##################################
    # class instantiation method - initializes instance variables
    #
    # usersItemRatings:
    # users item ratings data is in the form of a nested dictionary:
    # at the top level, we have User Names as keys, and their Item Ratings as values;
    # and Item Ratings are themselves dictionaries with Item Names as keys, and Ratings as values
    # Example: 
    #     {"Angelica":{"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
    #      "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}}
    #
    # metric:
    # metric is in the form of a string. it can be any of the following:
    # "minkowski", "cosine", "pearson"
    #     recall that manhattan = minkowski with r=1, and euclidean = minkowski with r=2
    # defaults to "pearson"
    #
    # r:
    # minkowski parameter
    # set to r for minkowski, and ignored for cosine and pearson
    #
    # k:
    # the number of nearest neighbors
    # defaults to 1
    #
    def __init__(self, usersItemRatings, metric='pearson', r=1, k=1):
        
        # set self.usersItemRatings
        self.usersItemRatings = usersItemRatings

        # set self.metric and self.similarityFn
        if metric.lower() == 'minkowski':
            self.metric = metric
            self.similarityFn = self.minkowskiFn
        elif metric.lower() == 'cosine':
            self.metric = metric
            self.similarityFn = self.cosineFn
        elif metric.lower() == 'pearson':
            self.metric = metric
            self.similarityFn = self.pearsonFn
        else:
            print ("    (DEBUG - metric not in (minkowski, cosine, pearson) - defaulting to pearson)")
            self.metric = 'pearson'
            self.similarityFn = self.pearsonFn
        
        # set self.r
        if (self.metric == 'minkowski'and r > 0):
            self.r = r
        elif (self.metric == 'minkowski'and r <= 0):
            print ("    (DEBUG - invalid value of r for minkowski (must be > 0) - defaulting to 1)")
            self.r = 1
            
        # set self.k
        if k > 0:   
            self.k = k
        else:
            print ("    (DEBUG - invalid value of k (must be > 0) - defaulting to 1)")
            self.k = 1
            
    
    #################################################
    # minkowski distance (dis)similarity - most general distance-based (dis)simialrity measure
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def minkowskiFn(self, userXItemRatings, userYItemRatings):
        
        distance = 0
        commonRatings = False 
        
        for item in userXItemRatings:
            # inlcude item rating in distance only if it exists for both users
            if item in userYItemRatings:
                distance += pow(abs(userXItemRatings[item] - userYItemRatings[item]), self.r)
                commonRatings = True
                
        if commonRatings:
            return round(pow(distance,1/self.r), 2)
        else:
            # no ratings in common
            return -2

    #################################################
    # cosince similarity
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def cosineFn(self, userXItemRatings, userYItemRatings):
        
        sum_xy = 0
        sum_x2 = 0
        sum_y2 = 0
        
        for item in userXItemRatings:
            if item in userYItemRatings:
                x = userXItemRatings[item]
                y = userYItemRatings[item]
                sum_xy += x * y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        
        denominator = math.sqrt(sum_x2) * math.sqrt(sum_y2)
        if denominator == 0:
            return -2
        else:
            return round(sum_xy / denominator, 3)

    #################################################
    # pearson correlation similarity
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def pearsonFn(self, userXItemRatings, userYItemRatings):
        
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        
        for item in userXItemRatings:
            if item in userYItemRatings:
                n += 1
                x = userXItemRatings[item]
                y = userYItemRatings[item]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
       
        if n == 0:
            return -2
        
        denominator = math.sqrt(sum_x2 - pow(sum_x, 2) / n) * math.sqrt(sum_y2 - pow(sum_y, 2) / n)
        if denominator == 0:
            return -2
        else:
            return round((sum_xy - (sum_x * sum_y) / n) / denominator, 2)
            

    #################################################
    # make recommendations for userX from the most similar k nearest neigibors (NNs)
    def recommendKNN(self, userX):
        
        # YOUR CODE HERE
        distance_user = {}
        sorted_users = []
        recommendations = {}
        weights = {}
        distance = {}
        final_list = []
        total_weight = 0
        #distance between users
        for user in self.usersItemRatings.keys():
            if (user != userX):
                distance_user[user] = self.similarityFn(self.usersItemRatings[userX],self.usersItemRatings[user])
        #print (distance_user)
        #calculating normalized values
        distance_user = self.rating_normalize(distance_user)        
        #print(distance_user)
        #sorting the users        
        sorted_users = self.sort_dict(distance_user)
        #print(sorted_users)
        #considering only the k-nearest neighbours
        k_nn = sorted_users[:self.k]
        #print(k_nn)
        
        for user in k_nn:
            for movie in self.usersItemRatings[user]:
                recommendations[movie] = 0
                distance[movie] = 0
        for user in k_nn:
            total_weight += distance_user[user]
        for user in k_nn:
            weights[user] = distance_user[user]/total_weight
        
        
        #weighted average calculation of rating
        for user in k_nn:
            #print(user)
            for movie in self.usersItemRatings[user]:
                if movie not in self.usersItemRatings[userX]:
                    print(user)                    
                    #print(movie)
                    #print(distance_user[user])
                    #print(self.usersItemRatings[user][movie])
                    recommendations[movie] +=  (weights[user])*(self.usersItemRatings[user][movie])
                    #print(recommendations[movie])
                    #print(recommendations[movie])
                    #distance[movie] +=  distance_user[user]
                    #print(distance[movie])
        #print(recommendations)
        #print(distance)               
        for movie in recommendations.keys():
            if (recommendations[movie] !=0):
                final_list.append((movie,round(recommendations[movie],2)))
        return (sorted(final_list,key=lambda x: x[1],reverse=True) )  
        
            
        # for given userX, get the sorted list of users - by most similar to least similar        
        
        # calcualte the weighted average item recommendations for userX from userX's k NNs
        
        # return sorted list of recommendations (sorted highest to lowest ratings)
        # example: [('Broken Bells', 2.64), ('Vampire Weekend', 2.2), ('Deadmau5', 1.71)]
        
        # once you are done coding this method, delete the pass statement below
        

    #function to sort dictionary keys by value
    def sort_dict(self,userX):
        if (self.metric.lower() == 'minkowski') :   
            return(sorted(userX,key=userX.get))
        else:
            return(sorted(userX,key=userX.get,reverse = True))
    
    #function to normalize cosine and pearson ratings    
    def rating_normalize(self,ratings):
        if (self.metric.lower() == 'cosine'or self.metric.lower() == 'pearson') :   
            for key in ratings.keys():
                ratings[key] = (ratings[key]+1)/2
        return (ratings)
            

        

