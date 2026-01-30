// first ill generate a laberinth
// show it
// meke it have 2 possible paths
// show it
// make then ill add obstacles via keyboard
// find the shortest path via a*
// show it

//importo mis librerias
#include <iostream>
#include <vector>
#include <random>
#include <algorithm>
#include <deque>
#include <cstdlib>

using namespace std;


//defino mis constantes
const int DX[4] = {-1, 1, 0, 0};
const int DY[4] = {0, 0, 1, -1};
// constantes para obstaculos
const int WALL = 1;
const int EMPTY = 0;
const int BUILDING = 2;
const int WATER = 3;
const int BLOCK = 4;
const int PATH = 7;


//genero un numero random para generar el laberinto
mt19937 rng(random_device{}());


// funcion para imprimir
void print(vector<vector<int>> &maze, int height, int width)
{
    // imprime los numeros para saber la poscicion
    cout << "    ";
    for (int j = 0; j < width; j++)
    {
        if (j < 10)
            cout << j << " ";
        else
            cout << j; // adjust spacing for >9
    }
    cout << "\n";


    // se imprime el laberinto con sus diferentes cosas
    for (int i = 0; i < height; i++)
    {
        if (i < 10)
            cout << i << "   ";
        else
            cout << i << "  ";

        for (int j = 0; j < width; j++)
        {
            if (maze[i][j] == 1)
            {
                cout << "\033[37m" << "██";
            }
            else if (maze[i][j] == 0)
            {
                cout << "  ";
            }
            else if (maze[i][j] == 2)
            {
                cout << "\033[30m" << "██" << "\033[37m";
            }
            else if (maze[i][j] == 3)
            {
                cout << "\033[34m" << "██" << "\033[37m";
            }
            else if (maze[i][j] == 4)
            {
                cout << "\033[31m" << "██" << "\033[37m";
            }
            else if (maze[i][j] == 5)
            {
                cout << "🚩";
            }
            else if (maze[i][j] == 6)
            {
                cout << "🏁";
            }
            else if (maze[i][j] == 7)
            {
                cout << "\033[33m" << "██" << "\033[37m";
            }
        }

        cout << "\n";
    }
}
//funciion p ara checkear que este adentro del laberinto y devuelve un booleano
bool inside(vector<vector<int>> maze, int width, int height, int x, int y)
{
    if (x >= 0 && x < width && y >= 0 && y < height && maze[y][x] != WALL)
    {
        return true;
    }
    else
    {
        return false;
    }
}
//se genera el laberinto random usando depth first search
void dfs(vector<vector<int>> &maze, int height, int width, int x, int y)
{
    deque<int> dirs = {0,1,2,3};

    shuffle(dirs.begin(),dirs.end(), rng);

    for(auto d: dirs){
        int nx = x + DX[d] *2;
        int ny = y + DY[d] *2;
        // if (!inside(maze,width,height,nx,ny))continue;
        if (nx < 0 || nx >= width || ny < 0 || ny >= height)
            continue;
        if (maze[ny][nx] != WALL)
            continue;

        maze[y + DY[d]][x + DX[d]] = EMPTY;
        maze[ny][nx] = EMPTY;

        dfs(maze,height,width,nx,ny);
        

    }

}

// esta funcion echa algunas paredes random para que haya mas de un camino 
//actually kinda dodgy but works
void hydra(vector<vector<int>> &maze, int height, int width)
{

    for (int k = 0; k < height; k++)
    {
        int x = rng() % width;
        int y = rng() % height;

        if (maze[y][x] != WALL)
            continue;
        int empty_neigbours = 0;
        for (int i = 0; i < 4; i++)
        {
            int nx = x + DX[i];
            int ny = y + DY[i];
            if (nx < 0 || nx >= width || ny < 0 || ny >= height)
                continue;
            if (maze[ny][nx] == 0)
                empty_neigbours++;
        }
        if (empty_neigbours == 2)//si tiene dos espacios a su alredesdor echa la pared
        {
            maze[y][x] = 0;
        }
    }
}
//funcion para ubicar obstaculos
void obstacles(vector<vector<int>> &maze, int height, int width)
{

    int x, y;
    int obstaculo;
    char coma;

    cout << "ingrese 1 para edificio, 2 para agua y 3 para zona bloqueada: ";
    cin >> obstaculo;

    cout << "ingrese cordenadas en x e y como x,y: ";
    cin >> x >> coma >> y;
    if (x >= 0 && x < width && y >= 0 && y < height && maze[y][x] != WALL)
    {
        if (obstaculo == 1)
        {
            maze[y][x] = 2;
        }
        else if (obstaculo == 2)
        {
            maze[y][x] = 3;
        }
        else if (obstaculo == 3)
        {
            maze[y][x] = 4;
        }
    }
}



// funcion que ubica las posiciones de inicio y meta si cumple con las condiciones
bool start_goal(vector<vector<int>> &maze, int width, int height, int start_x, int start_y, int end_x, int end_y)
{

    if (inside(maze, width, height, start_x, start_y) && inside(maze, width, height, end_x, end_y))
    {
        maze[start_y][start_x] = 5;
        maze[end_y][end_x] = 6;
        return false;
    }
    else
    {
        cout << "coordenadas invalidas, intente de nuevo ";
        return true;
    }
}




// funcion para recorrer el laberinto 

void A_star(vector<vector<int>> &maze, int height, int width,int start_x, int start_y,int end_x,int end_y){
    
    vector<vector<int>> g_cost(height, vector<int>(width,1e9));
    vector<vector<int>> f_cost(height, vector<int>(width,1e9));
    vector<vector<pair<int,int>>> parent(height, vector<pair<int,int>>(width,{-1,-1}));

    auto heuristic =[&](int x,int y){
        return abs(x - end_x) + abs(y - end_y);
    };

    g_cost[start_y][start_x] = 0;
    f_cost[start_y][start_x] = heuristic(start_x,start_y);
    vector<pair<int,int>> open_list;
    open_list.push_back({start_x,start_y});
    
    while (!open_list.empty()){
        int best_index = 0;
        for (size_t i = 1; i < open_list.size(); i++){
            int x = open_list[i].first;
            int y = open_list[i].second;
            int best_x = open_list[best_index].first;
            int best_y = open_list[best_index].second;
            if (f_cost[y][x] < f_cost[best_y][best_x]){
                best_index = i;
            }
            
        }

        int current_x = open_list[best_index].first;
        int current_y = open_list[best_index].second;

        open_list.erase(open_list.begin() + best_index);

        if (current_x ==  end_x && current_y == end_y)
        {
            break;
        }
        int tentative;
        for (int i = 0; i < 4; i++)
        {
            int new_x = current_x + DX[i];
            int new_y = current_y + DY[i];

            if(!inside(maze,width,height,new_x,new_y))continue;
            if(maze[new_y][new_x] == BUILDING)continue;
            if(maze[new_y][new_x] == BLOCK)continue;
            if(maze[new_y][new_x] == WATER){
                tentative = g_cost[current_y][current_x] + 2;
            }else{
                tentative = g_cost[current_y][current_x] + 1;

            }

            // int *puntero;
            // puntero = &tentative;


            if (tentative < g_cost[new_y][new_x] ){
                g_cost[new_y][new_x] = tentative;
                f_cost[new_y][new_x] = heuristic(new_x,new_y) + tentative;
                parent[new_y][new_x] = {current_x,current_y};

                open_list.push_back({new_x,new_y});
            }
             
        }
         

    }
    


    //reconstruccion de camino
    vector<pair<int,int>> path;

    int path_x = end_x;
    int path_y = end_y;

    while (!(path_x == start_x && path_y == start_y)){
        pair<int,int> prev = parent[path_y][path_x];

        if (prev.first == -1){
            cout << "no hay otro camino";
            break;
        }

        path.push_back({path_x,path_y});
        path_x  = prev.first;
        path_y = prev.second;
    }
    
    reverse(path.begin(), path.end());

    for (auto [x,y] : path){
        if (maze[y][x] == EMPTY){
            maze[y][x] = PATH;
        }

        system("cls");
        print(maze,height,width);
        
    }
    
}

//main function

int main()
{
    int x = 1;
    int y = 1;
    int height, width;
    char opcion;
    int start_x, start_y;
    int end_x, end_y;
    char coma;
    bool valid = true;

    cout << " ingrese altura del laberinto: ";
    cin >> height;
    cout << " ingrese ancho del laberinto: ";
    cin >> width;

    if (height % 2 == 0)
        height++;
    if (width % 2 == 0)
        width++;

    vector<vector<int>> maze(height, vector<int>(width, 1));

    dfs(maze, height, width, x, y);
    hydra(maze, height, width);
    print(maze, height, width);

    while (valid)//marcar coordenadas de entrada y salida en el laberinto
    {
        cout << "ingrese coordenadas de entrada  como x,y: ";
        cin >> start_x >> coma >> start_y;

        cout << "ingrese coordenadas de salida  como x,y: ";
        cin >> end_x >> coma >> end_y;
        valid = start_goal(maze, width, height, start_x, start_y, end_x, end_y);
    }
    print(maze, height, width);

    // solve it

    A_star(maze, height, width, start_x, start_y, end_x, end_y);

    while (opcion != 'n' && opcion != 'N')//poner obstaculos por teclado
    {
        cout << "deasea añadir obstaculos ? ( s/n ): ";
        cin >> opcion;
        if (opcion == 's' || opcion == 'S')
        {

            for (int i = 0; i < height; i++)
            {
                for (int j = 0; j < width; j++)
                {
                    if (maze[j][i] == 7)
                    {
                        maze[j][i] = EMPTY;
                    }
                }
            }

            obstacles(maze, height, width);
            print(maze, height, width);
        }
    }

    A_star(maze, height, width, start_x, start_y, end_x, end_y);

    return 0;
}