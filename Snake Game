#  Katherine Zhang
#  Viper: A competative variant of Snake
#
#  Goal: Be the last snake standing in each round.
#
#  Scoring: Each time a snake crashes all of the snakes that have not yet
#           crashed are awarded 1 point.
#
#  Game End: The game ends at the end of the round in which one or more players
#            reach 10 points.  The player with the highest score is the winner.
#            Ties can occur.
#
#  Future Work: Right now the AI identifies the direction it should head
#               by looking for the longest distance to a collision.  But it
#               doesn't check to see if it is possible to turn from its
#               current heading to the heading that has the longest distance
#               without colliding with anything.  It would be better if the
#               AI identified its direction based on the longest distance to
#               a collision that can actually be reached based on its turning
#               radius (which is based on its speed).
#
from SimpleGraphics import *
from math import sin, cos, tan, atan2, pi, sqrt, fabs, ceil
from random import randrange
from time import time
from functools import partial, reduce

FRAME_RATE = 30 # Target framerate to maintain
BOUNDARY = [0, 0, 799, 0, 799, 599, 0, 599, 0, 0] # Line segments for the edges
                                                  # of the screen

###############################################################################
##
##  Functions to determine whether or not two line segments intersect (and
##  where they intersect).  The only function that needs to be called directly
##  by a student is doIntersect.  The other functions are called by the
##  provided code.
##
##  Adapted from
##  https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
##
###############################################################################

#
# Do line segments (ax, ay, bx, by) and (cx, cy, dx, dy) intersect?
#
# Parameters:
#   (ax, ay, bx, by): The end points of the first line segment
#   (cx, cy, dx, dy): The end points of the second line segemnt
#
# Returns:
#   True if the line segments intersect, False otherwise.
#
def doIntersect(ax, ay, bx, by, cx, cy, dx, dy):
  return doIntersectPos(ax, ay, bx, by, cx, cy, dx, dy)[0]

#
# Determine if a point lies on a line segment.  The three points passed to
# this function must be co-linear.
#
# Parameters:
#   (px, py): One end point of the line segment
#   (qx, qy): The point to check
#   (rx, ry): The other end of the line segment
#
# Returns:
#   True if (qx, qy) lines on line segment (px, py, rx, ry).  False otherwise.
#
def onSegment(px, py, qx, qy, rx, ry):
  if qx <= px and qx <= rx and qx >= px and qx >= rx and \
     qy <= py and qy <= ry and qy >= py and qy >= ry:
    return True

  return False

#
# Do line segments (ax, ay, bx, by) and (cx, cy, dx, dy) intersect?  What is
# their intersection point?
#
# Parameters:
#   (ax, ay, bx, by): The end points of the first line segment
#   (cx, cy, dx, dy): The end points of the second line segemnt
#
# Returns:
#   True and the intersection point if the line segments intersect.  Otherwise
#   (False, 0, 0) is returned.
#
def doIntersectPos(ax, ay, bx, by, cx, cy, dx, dy):
  # Bounding box checks
  if ax < cx and ax < dx and bx < cx and bx < dx:
    return False, 0, 0
  if ax > cx and ax > dx and bx > cx and bx > dx:
    return False, 0, 0
  if ay < cy and ay < dy and by < cy and by < dy:
    return False, 0, 0
  if ay > cy and ay > dy and by > cy and by > dy:
    return False, 0, 0

  # Compute the orientation values.  This has been inlined to improve
  # performance.
  val = (by - ay) * (cx - bx) - (bx - ax) * (cy - by)
  o1 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  val = (by - ay) * (dx - bx) - (bx - ax) * (dy - by)
  o2 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  val = (dy - cy) * (ax - dx) - (dx - cx) * (ay - dy)
  o3 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  val = (dy - cy) * (bx - dx) - (dx - cx) * (by - dy)
  o4 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  # General case
  if o1 != o2 and o3 != o4:
    # If (ax, ay, bx, by) is vertical
    if ax == bx:
      m_cd = (dy - cy) / (dx - cx)
      b_cd = cy - m_cd * cx
      return (True, ax, m_cd * ax + b_cd)

    # If (cx, cy, dx, dy) is vertical
    if cx == dx:
      m_ab = (by - ay) / (bx - ax)
      b_ab = ay - m_ab * ax
      return (True, cx, m_ab * cx + b_ab)

    # This can't be computed earlier in case bx - ax is 0, or dx - cx is 0
    m_ab = (by - ay) / (bx - ax)
    b_ab = ay - m_ab * ax
    m_cd = (dy - cy) / (dx - cx)
    b_cd = cy - m_cd * cx

    # If m_cd + m_ab is 0 or b_ab is 0 then we have to handle it as a special
    # case
    if m_cd + m_ab == 0 or b_ab == 0:
      y = -(m_ab * b_cd + m_cd * b_ab) / (m_cd - m_ab)
      x = (y - b_ab) / m_ab
      return (True, x, y)

    # General case
    x = (b_cd - b_ab) / (m_ab - m_cd)
    y = m_ab * x + b_ab
    return (True, x, y)

  # Special Cases
  # a, b and c are colinear and c lies on segment ab
  if o1 == 0 and onSegment(ax, ay, cx, cy, bx, by):
    return (True, cx, cy)

  # a, b and d are colinear and d lies on segment ab
  if o2 == 0 and onSegment(ax, ay, dx, dy, bx, by):
    return (True, dx, dy)

  # c, d and a are colinear and a lies on segment cd
  if o3 == 0 and onSegment(cx, cy, ax, ay, dx, dy):
    return (True, ax, ay)

  # c, d and b are colinear and b lies on segment cd
  if o4 == 0 and onSegment(cx, cy, bx, by, dx, dy):
    return (True, bx, by)

  return (False, 0, 0) # Doesn't fall in any of the above cases

#
# Do line segments (ax, ay, bx, by) and (cx, cy, dx, dy) intersect?  What is
# their intersection point?  How far is (ax, ay) from the intersection point?
#
# This function largely duplicates doIntersectPos, but this version takes the
# second segment as a tuple to make it possible to map it over a list of such
# segments.  It only returns the distance to the intersection point (in
# addition to whether or not there was an intersection and its location) so
# that the minimum distance can be found with the min function.  This function
# doesn't call doIntersectPos to improve its performance.
#
# Parameters:
#   (ax, ay, bx, by): The end points of the first line segment
#   (seg): The end points of the second line segemnt as a tuple
#
# Returns:
#   The square of the distance from (ax, ay) to the intersection point (or
#     1e12 if they do not intersect)
#   True and the intersection point if the line segments intersect.  Otherwise
#   (False, 0, 0) is returned.
#
def doIntersectDistPos(ax, ay, bx, by, seg):
  cx, cy, dx, dy = seg

  # Bounding box checks
  if ax < cx and ax < dx and bx < cx and bx < dx:
    return 1e12, False, 0, 0
  if ax > cx and ax > dx and bx > cx and bx > dx:
    return 1e12, False, 0, 0
  if ay < cy and ay < dy and by < cy and by < dy:
    return 1e12, False, 0, 0
  if ay > cy and ay > dy and by > cy and by > dy:
    return 1e12, False, 0, 0

  # Compute the orientation values.  This has been inlined to improve
  # performance.
  val = (by - ay) * (cx - bx) - (bx - ax) * (cy - by)
  o1 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  val = (by - ay) * (dx - bx) - (bx - ax) * (dy - by)
  o2 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  val = (dy - cy) * (ax - dx) - (dx - cx) * (ay - dy)
  o3 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  val = (dy - cy) * (bx - dx) - (dx - cx) * (by - dy)
  o4 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  # General case
  if o1 != o2 and o3 != o4:
    # If (ax, ay, bx, by) is vertical
    if ax == bx:
      m_cd = (dy - cy) / (dx - cx)
      b_cd = cy - m_cd * cx
      x, y = ax, m_cd * ax + b_cd
      return (dist2(ax, ay, x, y), True, x, y)

    # If (cx, cy, dx, dy) is vertical
    if cx == dx:
      m_ab = (by - ay) / (bx - ax)
      b_ab = ay - m_ab * ax
      x, y = cx, m_ab * cx + b_ab
      return (dist2(ax, ay, x, y), True, x, y)

    # This can't be computed earlier in case bx - ax is 0, or dx - cx is 0
    m_ab = (by - ay) / (bx - ax)
    b_ab = ay - m_ab * ax
    m_cd = (dy - cy) / (dx - cx)
    b_cd = cy - m_cd * cx

    # If m_cd + m_ab is 0 or b_ab is 0 then we have to handle it as a special
    # case
    if m_cd + m_ab == 0 or b_ab == 0:
      y = -(m_ab * b_cd + m_cd * b_ab) / (m_cd - m_ab)
      x = (y - b_ab) / m_ab
      return (dist2(ax, ay, x, y), True, x, y)

    # General case
    x = (b_cd - b_ab) / (m_ab - m_cd)
    y = m_ab * x + b_ab
    return (dist2(ax, ay, x, y), True, x, y)

  # Special Cases
  # a, b and c are colinear and c lies on segment ab
  if o1 == 0 and onSegment(ax, ay, cx, cy, bx, by):
    return (dist2(ax, ay, cx, cy),True, cx, cy)

  # a, b and d are colinear and d lies on segment ab
  if o2 == 0 and onSegment(ax, ay, dx, dy, bx, by):
    return (dist2(ax, ay, dx, dy), True, dx, dy)

  # c, d and a are colinear and a lies on segment cd
  if o3 == 0 and onSegment(cx, cy, ax, ay, dx, dy):
    return (0, True, ax, ay)

  # c, d and b are colinear and b lies on segment cd
  if o4 == 0 and onSegment(cx, cy, bx, by, dx, dy):
    return (dist2(ax, ay, bx, by), True, bx, by)

  return (1e12, False, 0, 0) # Doesn't fall in any of the above cases

#
# Do line segments (ax, ay, bx, by) and (cx, cy, dx, dy) intersect?
#
# This function largely duplicates doIntersectPos, but this version takes the
# second segment as a tuple to make it possible to map it over a list of such
# segments.  It only returns whether or not there was an intersection, not it's
# position, so that a list of Booleans (that can have an and or or operation
# applied to them) is the result of such a map.  This function doesn't call
# doIntersectPos to improve its performance.
#
# Parameters:
#   (ax, ay, bx, by): The end points of the first line segment
#   seg: The end points of the second line segemnt (as a tuple)
#
# Returns: True and the intersection point if the line segments intersect.
# Otherwise (False, 0, 0) is returned.
#
def doIntersectTuple(ax, ay, bx, by, seg):
  cx, cy, dx, dy = seg

  # Bounding box checks
  if ax < cx and ax < dx and bx < cx and bx < dx:
    return False
  if ax > cx and ax > dx and bx > cx and bx > dx:
    return False
  if ay < cy and ay < dy and by < cy and by < dy:
    return False
  if ay > cy and ay > dy and by > cy and by > dy:
    return False

  # Compute the orientation values.  This has been inlined to improve
  # performance.
  val = (by - ay) * (cx - bx) - (bx - ax) * (cy - by)
  o1 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  val = (by - ay) * (dx - bx) - (bx - ax) * (dy - by)
  o2 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  val = (dy - cy) * (ax - dx) - (dx - cx) * (ay - dy)
  o3 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  val = (dy - cy) * (bx - dx) - (dx - cx) * (by - dy)
  o4 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  # General case
  if o1 != o2 and o3 != o4:
    # If (ax, ay, bx, by) is vertical
    if ax == bx:
      m_cd = (dy - cy) / (dx - cx)
      b_cd = cy - m_cd * cx
      return True

    # If (cx, cy, dx, dy) is vertical
    if cx == dx:
      m_ab = (by - ay) / (bx - ax)
      b_ab = ay - m_ab * ax
      return True

    # This can't be computed earlier in case bx - ax is 0, or dx - cx is 0
    m_ab = (by - ay) / (bx - ax)
    b_ab = ay - m_ab * ax
    m_cd = (dy - cy) / (dx - cx)
    b_cd = cy - m_cd * cx

    # If m_cd + m_ab is 0 or b_ab is 0 then we have to handle it as a special
    # case
    if m_cd + m_ab == 0 or b_ab == 0:
      y = -(m_ab * b_cd + m_cd * b_ab) / (m_cd - m_ab)
      x = (y - b_ab) / m_ab
      return True

    # General case
    x = (b_cd - b_ab) / (m_ab - m_cd)
    y = m_ab * x + b_ab
    return True

  # Special Cases
  # a, b and c are colinear and c lies on segment ab
  if o1 == 0 and onSegment(ax, ay, cx, cy, bx, by):
    return True

  # a, b and d are colinear and d lies on segment ab
  if o2 == 0 and onSegment(ax, ay, dx, dy, bx, by):
    return True

  # c, d and a are colinear and a lies on segment cd
  if o3 == 0 and onSegment(cx, cy, ax, ay, dx, dy):
    return True

  # c, d and b are colinear and b lies on segment cd
  if o4 == 0 and onSegment(cx, cy, bx, by, dx, dy):
    return True

  return False # Doesn't fall in any of the above cases

###############################################################################
##
##  End of code for determining whether or not two line segments intersect.
##
###############################################################################

###############################################################################
##
##  Other functions used by the provided code.
##
###############################################################################

#
# Compute and return the distance between two points.
#
# Parameters:
#   (x1, y1): The first point
#   (x2, y2): The second point
#
# Returns:
#   The distance from (x1, y1) to (x2, y2)
#
def dist(x1, y1, x2, y2):
  return sqrt((x2-x1) * (x2-x1) + (y2-y1) * (y2-y1))

#
# Compute and return the square of the distance between two points.  (This
# function can be used when we just need to know if one distance is
# larger than another without knowing what the actual distances are.  It
# is more efficient than using dist because the square root doesn't need
# to be computed).
#
# Parameters:
#   (x1, y1): The first point
#   (x2, y2): The second point
#
# Returns:
#   The distance from (x1, y1) to (x2, y2)
#
def dist2(x1, y1, x2, y2):
  return (x2-x1) * (x2-x1) + (y2-y1) * (y2-y1)

#
# Does a line segment collide with any of the line segments represented by a
# list of points?  Functional constructs are used in an effort to maximize
# the performance of this function.
#
# Parameters:
#   (ax, ay), (bx, by): A line segment
#   segments: A list of points [x0, y0, x1, y1, x2, y2, ... , xn, yn]
#
# Returns:
#   True if (ax, ay), (bx, by) intersects with any of the line segments
#   represented by adjacent points in the list.  False otherwise.
#
def fastCollides(ax, ay, bx, by, segments):
  it = iter(segments)
  it2 = iter(segments)
  if len(segments) >= 2:
    next(it2)
    next(it2)
  # Are the above 4 lines faster than it2 = iter(segments[2:])?  That
  # probably depends on the length of segments.

  endpts = list(zip(it, it, it, it)) + list(zip(it2, it2, it2, it2))

  full = map(partial(doIntersectTuple, ax, ay, bx, by), endpts)
  return reduce((lambda x, y: x or y), full, False)

#
# Find and return the location of the closest collision to (ax, ay) between the
# line segment (ax, ay), (bx, by) and any segment in a list of list of list of
# points.  Functional constructs are used in an effort to maximize the
# performance of this function.
#
# Parameters:
#   (ax, ay), (bx, by): A line segment
#   segments: A list of lists, each of which is a list of points [x0, y0, x1,
#             y1, x2, y2, ... , xn, yn]
#
# Returns:
#   True if (ax, ay), (bx, by) intersects with any of the line segments
#   represented by adjacent points in the lists.  False otherwise.
#   The (x, y) location of the intersection point
#
def closestCollision(ax, ay, bx, by, seg_lists):
  full = []
  for segs in seg_lists:
    it = iter(segs)
    it2 = iter(segs)
    if len(segs) >= 2:
      next(it2)
      next(it2)
    # Are the above 4 lines faster than it2 = iter(segments[2:])?  That
    # probably depends on the length of segments.

    endpts = list(zip(it, it, it, it)) + list(zip(it2, it2, it2, it2))

    # Not sure if += or extend is faster
    #full.extend(map(partial(doIntersectDistPos, ax, ay, bx, by), endpts))
    full += map(partial(doIntersectDistPos, ax, ay, bx, by), endpts)

  mn = min(full)
  if mn[1] == False:
    return (False, 0, 0)
  else:
    return (True, mn[2], mn[3])

#
# Display the countdown used before the game starts and between rounds.  This
# function doesn't return until the countdown is complete.
#
# Parameters:
#   duration: The duration of the countdown in seconds
#
# Returns:
#   None
#
def countdown(duration):
  start = time()
  end = start + duration

  setFont("Arial", 30)
  setColor("black")

  while not closed() and time() < end:
    clear()
    text(getWidth() / 2, getHeight() / 2, ceil(end - time()), "c")
    update()

#
# Get the number of AI players for the user.
#
# Parameters:
#   (None)
#
# Returns:
#   The number of players selected by the user
#
def getAICount():
  setFont("Arial", 30)
  setColor("black")
  text(getWidth() / 2, 200, "Python Viper")

  text(300, 500, "1")
  text(400, 500, "2")
  text(500, 500, "3")

  setFont("Arial", 15)
  setColor("black")
  text(getWidth() / 2, 400, "Select the number of AI snakes to begin the game.")

  setFont("Arial", 12)
  text(getWidth() / 2, 575, "Note that slower machines may struggle to achieve a reasonable framerate with more than one AI snake.")


  setOutline("gray50")
  setFill(None)
  for i in range(3):
    rect(275 + i * 100, 475, 50, 50)

  num_ai = 0
  while not closed() and num_ai == 0:
    if leftButtonPressed():
      x, y = mousePos()

      for i in range(3):
        if x >= 275 + i * 100 and x <= 275 + i * 100 + 50 and \
           y >= 475 and y <= 475 + 50:
          num_ai = i + 1

  return num_ai

###############################################################################
##
##  Insert the functions that you need to write in parts 3 and 5 here.
##
###############################################################################
#   Part 3
# This function subtracts points from the snake body if it exceeds the maximum length.
# Parameters: length of the snake, maximum length allowed
# Returns: length of the snake, maximum length allowed
def movingsnake(p1queue, maxlength):
    # Initializing the total distance between points to zero
    pointdistance = 0
    # If the number of points is greater than 4
    if 4 <= len(p1queue):
        for i in range(0, len(p1queue)//2-1):
            # If the distance is less than the max length, add the distance to the total distance
            if pointdistance <= maxlength:
                pointdistance = pointdistance + sqrt((p1queue[i] - p1queue[i+2]) ** 2 + (p1queue[i+1] - p1queue[i+3]) ** 2)
            # If the distance is greater than the max length, subtract the distance between the oldest points and remove the oldest points.
            else:
                pointdistance = pointdistance - sqrt((p1queue[0] - p1queue[2]) ** 2 + (p1queue[1] - p1queue[3]) ** 2)
                p1queue.pop(0)
                p1queue.pop(0)
    return p1queue, maxlength

#   Part 5
# This function determines if the head of the snake intersects with any other line
# segment on the snake body by calling the doIntersect function.
# Parameters: endpoints of most recent line segments, list of points of snake
# Returns: a boolean value depending if doIntersect is true or false.
def collideYourself(x1, y1, x2, y2, queue):
    for i in range(0, len(queue)-6, 2):
        if doIntersect(x1, y1, x2, y2, queue[i], queue[i+1], queue[i+2], queue[i+3]):
            return True
    return False

###############################################################################
##
##  End of function insertion point.
##
###############################################################################

# Play the game
def main():
  # Only redraw the screen when specifically requested to do so
  setAutoUpdate(False)

  counter = 0             # Frame counter
  speed = 100             # Snake speeds in pixels per second
  max_length = 100        # Current maximum length for the snakes
  time_since_increase = 0 # How much time has elapsed since the last time the
                          # speed was increased and the snakes were lengthened?

  # Create the player snake

  # Randomly position the player in the upper left corner of the screen and
  # point them toward the middle of the screen
  p1_x = randrange(5, getWidth() // 4 - 1)
  p1_y = randrange(5, getHeight() // 4 - 1)
  p1_heading = atan2(getHeight() / 2 - p1_y, getWidth() / 2 - p1_x)

  p1_lost = False   # Has the player lost?
  p1_plost = False  # Previous frame's lost value
  p1_queue = []     # x1, y1, x2, y2, ..., xn, yn
  p1_score = 0      # The player's sore

  # Get the number of AI players from the user
  num_ai = getAICount()

  # Set up each list so that it is populated with 3 values, then truncate the
  # number of values in the list to the number of AI players selected for the
  # game.
  if num_ai > 0:
    e_queues = [[randrange(3 * getWidth() // 4 + 1, getWidth() - 1), \
                 randrange(3 * getHeight() // 4 + 1, getHeight() - 1)], \
                [randrange(3 * getWidth() // 4 + 1, getWidth() - 1),
                 randrange(5, 1 * getHeight() // 4 - 1)], \
                [randrange(5, 1 * getWidth() // 4 - 1),
                 randrange(3 * getHeight() // 4 + 1, getHeight() - 1)]][:num_ai]
    e_lengths = [0, 0, 0][:num_ai]
    e_scores = [0, 0, 0][:num_ai]
    e_names = ["Roomba", "R2-D2", "Lt. Cmdr. Data"][:num_ai]
    e_colors = ["Blue", "Green", "Dark Orange"][:num_ai]
    e_lost = [False, False, False][:num_ai]
    e_plost = [False, False, False][:num_ai]

    # Compute each AI snake's initial heading
    e_headings = []
    for i in range(len(e_queues)):
      e_headings.append(atan2(getHeight() / 2 - e_queues[i][1], \
                        getWidth() / 2 - e_queues[i][0]))

  # Get ready to play!
  countdown(3)
  state = "playing"

  # Make the snakes wider so they are easier to see
  setWidth(3)
  reset_time = 0

  # Set up initial values for the frame rate timing
  start = time()
  elapsed = 1/FRAME_RATE

  # While the game has not been closed.  TODO: Right now there is a break
  # inside the loop to get out and report the winner.  This should be
  # improved.
  while not closed():
    if state == "next_round" and time() > reset_time:

      # TODO: Being lazy -- this should be handled in a better way
      max_score = max([p1_score] + e_scores)
      if max_score >= 10:
        break;

      # Reset the maximum length and speed
      speed = 100        # snake speeds in pixels per second
      max_length = 100   # current maximum length for the snakes

      # Set the player up to play again
      p1_x = randrange(5, getWidth() // 4 - 1)
      p1_y = randrange(5, getHeight() // 4 - 1)
      p1_heading = atan2(getHeight() / 2 - p1_y, getWidth() / 2 - p1_x)
      p1_lost = False
      p1_plost = False  # Previous frame's lost value
      p1_queue = []

      # Set the AI players up to play again
      e_queues = [[randrange(3 * getWidth() // 4 + 1, getWidth() - 1), \
                   randrange(3 * getHeight() // 4 + 1, getHeight() - 1)], \
                  [randrange(3 * getWidth() // 4 + 1, getWidth() - 1),
                   randrange(5, 1 * getHeight() // 4 - 1)], \
                  [randrange(5, 1 * getWidth() // 4 - 1),
                   randrange(3 * getHeight() // 4 + 1, getHeight() - 1)]][:num_ai]
      e_lengths = [0, 0, 0][:num_ai]
      e_lost = [False, False, False][:num_ai]
      e_plost = [False, False, False][:num_ai]

      # Compute each AI snake's initial heading
      e_headings = []
      for i in range(len(e_queues)):
        e_headings.append(atan2(getHeight() / 2 - e_queues[i][1], \
                          getWidth() / 2 - e_queues[i][0]))

      # Prepare for the next round
      countdown(3)
      state = "playing"

      # Reset the timer
      start = time()
      elapsed = 1/FRAME_RATE


    clear()

    # Draw the player snake if it consists of at least one line segment
    if p1_lost == True:
      setColor("red")
    else:
      setColor("black")
    ellipse(p1_x - 2, p1_y - 2, 5, 5)
    if 'p1_queue' in locals() and len(p1_queue) >= 4:
      line(p1_queue)

    for i in range(len(e_queues)):
      if len(e_queues[i]) >= 4:
        if e_lost[i] == True:
          setColor("red")
        else:
          setColor(e_colors[i])
        line(e_queues[i])
        ellipse(e_queues[i][-2] - 2, e_queues[i][-1] - 2, 5, 5)

    # Read input
    keys = getHeldKeys()

    # Update the display values
    setFont("Arial", 10)
    setColor("Black")
    text(5, 530, "Speed: " + str(round(speed,1)), "w")
    text(5, 545, "Max Length: " + str(max_length), "w")
    text(5, 560, "Frame rate: " + str(round(1 / elapsed,2)), "w")

    # Respond to the input and update the player's position if they haven't lost
    #if p1_lost == False:
    if "Left" in keys:
      p1_heading = p1_heading - pi * elapsed
    if "Right" in keys:
      p1_heading = p1_heading + pi * elapsed

###############################################################################
##
##  Insert your code for parts 1 through 6 here.  This code runs once for
##  each frame in the game (approximately 30 times a second).  The insertion
##  point for functions that you need to write is marked above.
##
###############################################################################
    if p1_lost == False:
    #  Part 1: A Moving Dot...
        p1_x = p1_x + cos(p1_heading) * speed * elapsed
        p1_y = p1_y + sin(p1_heading) * speed * elapsed

    #  Part 2: A Growing but Permanent Line
        # Adding a new x and y value to the end of the list
        p1_queue.append(p1_x)
        p1_queue.append(p1_y)

    #  Part 3: A Moving Snake
        movingsnake(p1_queue, max_length)

    #  Part 4: Colliding with the Walls
    if (p1_x > 799 or p1_x < 0) or (p1_y > 599 or p1_y < 0):
        # if the snake goes outside the screen, the player loses
        p1_lost = True

    #  Part 5
    if len(p1_queue) >= 4 and p1_lost == False:
        # Setting the x and y values to the most recently added points on the snake
        x1 = p1_queue[-2]
        y1 = p1_queue[-1]
        x2 = p1_queue[-4]
        y2 = p1_queue[-3]
        # Setting p1_lost to the boolean value of the collision function
        p1_lost = collideYourself(x1, y1, x2, y2, p1_queue[0:len(p1_queue) - 4])

# Part 6
	if len(e_queues) >= 4 and p1_lost == False:
    	for ai_snakes in range(len(e_queues)):
    		for point in range(len(ai_snakes)):
    			p1_lost = collideYourself(x1, y1, x2, y2, e_queues[ai_snakes][point])
        	

###############################################################################
##
##  Do not modify the code that follows unless you are attempting one of the
##  bonus parts of the assignment.
##
###############################################################################

    # Respond to the input and update the AI's position if they haven't lost
    for i in range(len(e_queues)):
      if e_lost[i] == False:
        # Avoid colliding with ourselves due to overlap between the current
        # segment touching the end of the previous one
        most_e_queue = e_queues[i][:-2]

        # Need the other two snakes so that we can check if we collided with them
        # Construct a list of the other snakes, and add to their heads to
        # make cut-offs harder
        others = list(e_queues)
        for j in range(len(e_queues)):
          ox = others[j][-2] + cos(e_headings[j]) * speed * 0.6
          oy = others[j][-1] + sin(e_headings[j]) * speed * 0.6
          others[j] = others[j] + [ox, oy]

        others.pop(i)

        # Extend the player's queue to make it harder for the player to cut the
        # AI off
        if 'p1_queue' in locals() and len(p1_queue) > 0:
          extended_p1_queue = p1_queue + [p1_queue[-2] + cos(p1_heading) * speed * 0.6, p1_queue[-1] + sin(p1_heading) * speed * 0.6]
        else:
          extended_p1_queue = []

        angle = e_headings[i] - 0.6 * pi
        found = False
        while angle <= e_headings[i] + 0.6 * pi:
          (hits, x, y) = closestCollision(e_queues[i][-2], e_queues[i][-1], e_queues[i][-2] + cos(angle) * 10000, e_queues[i][-1] + sin(angle) * 10000, [extended_p1_queue, most_e_queue, BOUNDARY] + others)

          if hits == False:
            # This should never happen becase we should always at least hit
            # the boundary
            print(e_queues[i][-2], e_queues[i][-1], e_queues[i][-2] + cos(angle) * 2000, e_queues[i][-1] + sin(angle) * 2000)
            raise("hits is False when that shouldn't be possible")

          if hits and found == False:
            best_x = x
            best_y = y
            best_angle = angle
            found = True
          elif hits and found:
            if dist2(e_queues[i][-2], e_queues[i][-1], x, y) > dist2(e_queues[i][-2], e_queues[i][-1], best_x, best_y):
              best_x = x
              best_y = y
              best_angle = angle

          angle += 0.05 * pi

        old_heading = e_headings[i]

        if e_headings[i] < -pi / 2 and best_angle > pi / 2:
          best_angle -= 2 * pi
        if e_headings[i] > pi / 2 and best_angle < -pi / 2:
          best_angle += 2 * pi

        if e_headings[i] < best_angle:
          if best_angle - e_headings[i] < pi * elapsed:
            e_headings[i] = best_angle
          else:
            e_headings[i] = e_headings[i] + pi * elapsed
        elif e_headings[i] > best_angle:
          if e_headings[i] - best_angle < pi * elapsed:
            e_headings[i] = best_angle
          else:
            e_headings[i] = e_headings[i] - pi * elapsed

        e_headings[i] %= 2*pi

        ex = e_queues[i][-2] + cos(e_headings[i]) * speed * elapsed
        ey = e_queues[i][-1] + sin(e_headings[i]) * speed * elapsed

        # Determine if the AI has crashed into any AI (including itself)
        for j in range(len(e_queues)):
          if i == j:
            if fastCollides(e_queues[i][-2], e_queues[i][-1], ex, ey, e_queues[j][:-2]):
              e_lost[i] = True
          else:
            if fastCollides(e_queues[i][-2], e_queues[i][-1], ex, ey, e_queues[j]):
              e_lost[i] = True


        # Determine if the AI has crashed into the player
        if 'p1_queue' in locals():
          if fastCollides(e_queues[i][-2], e_queues[i][-1], ex, ey, p1_queue):
            e_lost[i] = True

        # Determine if the player has crashed into a wall
        if fastCollides(e_queues[i][-2], e_queues[i][-1], ex, ey, BOUNDARY):
          e_lost[i] = True

        # Add the latest segment to the snake and truncate it to the correct
        # length
        e_queues[i].append(ex)
        e_queues[i].append(ey)
        e_lengths[i] += dist(e_queues[i][-4], e_queues[i][-3], e_queues[i][-2], e_queues[i][-1])
        while e_lengths[i] > max_length:
          e_lengths[i] -= dist(e_queues[i][0], e_queues[i][1], e_queues[i][2], e_queues[i][3])
          # Is this faster than popping two elements from the front of the list?
          e_queues[i] = e_queues[i][2:]

    # Increase the speeds and lengths of the snakes
    time_since_increase += elapsed
    if time_since_increase > 0.1:
      time_since_increase -= 0.1
      speed += 0.1
      max_length += 2

    # If the player's lost status changed during this frame
    if p1_lost != p1_plost:
      # Give a point to every AI that is still alive
      for j in range(len(e_queues)):
        if e_lost[j] == False:
          e_scores[j] += 1

    # If any of the enemy's list status changed during this frame
    for i in range(len(e_queues)):
      if e_lost[i] != e_plost[i]:
        # Give a point to the player if they are still alive
        if p1_lost == False:
          p1_score += 1

        # Give a point to every AI that is still alive
        for j in range(len(e_queues)):
          if e_lost[j] == False:
            e_scores[j] += 1

    # Display the scores
    setColor("Black")
    setFont("Arial", 15)
    text(10, getHeight() - 20, "Human: " + str(p1_score), "w")
    for j in range(len(e_scores)):
      setColor(e_colors[j])
      text((j + 1) * getWidth() / (len(e_scores) + 1), getHeight() - 20, e_names[j] + ": " + str(e_scores[j]), "w")

    # Determine if the game has been won by counting the number of players
    # that have not lost
    if state == "playing":
      winner_count = 0
      if p1_lost == False:
        winner_count += 1
        winner = "Human"
      for i in range(len(e_lost)):
        if e_lost[i] == False:
          winner_count += 1
          winner = e_names[i]

      if winner_count <= 1:
        state = "next_round"
        reset_time = time() + 3


    # Update the previous lost status to match the current lost status for the
    # player and all of the AIs
    p1_plost = p1_lost
    for i in range(len(e_queues)):
      e_plost[i] = e_lost[i]

    # Count the frame
    counter += 1

    if winner_count == 0 and state == "next_round":
      setFont("Arial", 30)
      setColor("black")
      text(getWidth() / 2, getHeight() / 2, "This Round Ended in a Draw")
    elif winner_count == 1 and state == "next_round":
      setFont("Arial", 30)
      setColor("black")
      text(getWidth() / 2, getHeight() / 2, "This Round was Won by " + winner)

    # Update the screen
    update()

    # Delay so that the current frame took 1/FRAME_RATE of a second
    current = time()
    elapsed = current - start
    while elapsed < 1 / FRAME_RATE:
      current = time()
      elapsed = current - start

    # Record the start time for the next frame
    start = current

  if not closed():
    # Find the winner of the game
    winner = ""
    if p1_score == max_score:
      winner = "Human"

    for i in range(len(e_scores)):
      if e_scores[i] == max_score:
        if winner == "":
          winner = e_names[i]
        else:
          winner += " and " + e_names[i]

    # Report the winner of the game
    while not closed():
      clear()
      setFont("Arial", 30)
      text(getWidth() / 2, getHeight() / 2 - 30, "Game Over!")
      text(getWidth() / 2, getHeight() / 2 + 30, "The game was won by " + winner)
      update()

main()
