# **Request Data**
## **Rating Prediction**
- Domain/Segment
- Game
- Total rounds/Total Games
- Kill-Death Ratio/ Win-Loss Ratio

## **Incremental Learning**
- Domain/Segment
- Game
- Total rounds/Total Games
- Kill-Death Ratio/ Win-Loss Ratio
- Rating

## **Recommendation**
### *Player Recommendations*
- Data : [Segment, Game, Total Rounds/Total Games, Kill-Death Ratio/ Win-Loss Ratio, Rating] of players as a Dictionary.
- Player ID: Current User
- Number of Recommendations to generate (default=5 for Alpha)

### *Post/Feed Recommendations*
- Player Data: [Segment, Game] as a Dictionary.
- Post/Feed Data: [Segment, Game, Post ID, Post Tags, Post Dates] as a Dictionary.
- Number of Posts

#
#

# **Response Data**
## **Rating Prediction**
- Player Rating

## **Incremental Learning**
- No Response Data

## **Recommendation**
## *Player Recommendations*
- List of recommended Player IDs.

### *Post/Feed Recommendations*
- List of recommended Post IDs.

