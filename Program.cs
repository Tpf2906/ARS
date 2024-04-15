using System;
using System.Collections.Generic;

class MazeGenerator
{
    private int width;
    private int height;
    private int[,] maze;
    private bool[,] visited;
    private Random random;

    public MazeGenerator(int width, int height)
    {
        this.width = width + 2; // Added 2 for a border on each side
        this.height = height + 2;
        maze = new int[this.width, this.height];
        visited = new bool[this.width, this.height];
        random = new Random();
        Initialize();
    }

    private void Initialize()
    {
        // Set all cells to walls
        for (int i = 0; i < width; i++)
        {
            for (int j = 0; j < height; j++)
            {
                maze[i, j] = 1;
            }
        }
    }

    public void GenerateMaze(int startX, int startY, int currentX, int currentY, int rewardX, int rewardY)
    {
        visited[currentX, currentY] = true;
        if (currentX > 0 && currentX < width - 1 && currentY > 0 && currentY < height - 1)
        {
            maze[currentX, currentY] = 0;
        }

        List<(int, int)> neighbors = GetNeighbors(currentX, currentY);
        Shuffle(neighbors);
        foreach (var neighbor in neighbors)
        {
            int x = neighbor.Item1;
            int y = neighbor.Item2;

            if (!visited[x, y])
            {
                visited[x, y] = true;
                if (x > 0 && x < width - 1 && y > 0 && y < height - 1)
                {
                    maze[x, y] = 0;
                    ConnectCells(currentX, currentY, x, y);
                }
                GenerateMaze(startX, startY, x, y, rewardX, rewardY);
            }
        }

        // Ensure reward and agent are not placed on the border
        if (rewardX > 0 && rewardX < width - 1 && rewardY > 0 && rewardY < height - 1)
            maze[rewardX, rewardY] = 2; 

        if (startX > 0 && startX < width - 1 && startY > 0 && startY < height - 1)
            maze[startX, startY] = 4;
    }

    private List<(int, int)> GetNeighbors(int x, int y)
    {
        List<(int, int)> neighbors = new List<(int, int)>();

        if (x > 1 && !visited[x - 2, y])
            neighbors.Add((x - 2, y));
        if (y > 1 && !visited[x, y - 2])
            neighbors.Add((x, y - 2));
        if (x < width - 2 && !visited[x + 2, y])
            neighbors.Add((x + 2, y));
        if (y < height - 2 && !visited[x, y + 2])
            neighbors.Add((x, y + 2));

        return neighbors;
    }

    private void ConnectCells(int x1, int y1, int x2, int y2)
    {
        // Connect cells without affecting the border
        if ((x1 + x2) / 2 > 0 && (x1 + x2) / 2 < width - 1 && (y1 + y2) / 2 > 0 && (y1 + y2) / 2 < height - 1)
            maze[(x1 + x2) / 2, (y1 + y2) / 2] = 0;
    }

    private void Shuffle<T>(List<T> list)
    {
        int n = list.Count;
        while (n > 1)
        {
            n--;
            int k = random.Next(n + 1);
            T value = list[k];
            list[k] = list[n];
            list[n] = value;
        }
    }

    public void PrintMaze()
    {
        for (int i = 0; i < height; i++)
        {
            for (int j = 0; j < width; j++)
            {
                Console.Write(maze[j, i] + " ");
            }
            Console.WriteLine();
        }
    }
}

class Program
{
    static void Main(string[] args)
    {
        int width = 40;
        int height = 40;
        int startX = 1; // Start away from the border
        int startY = 1;
        int rewardX = width - 2; // Place reward away from the border
        int rewardY = height - 2;

        MazeGenerator mazeGenerator = new MazeGenerator(width, height);
        mazeGenerator.GenerateMaze(startX, startY, startX, startY, rewardX, rewardY);
        mazeGenerator.PrintMaze();
    }
}
