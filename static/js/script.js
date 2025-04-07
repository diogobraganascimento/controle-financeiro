// Plugin para mostrar o texto central no gráfico (Total)
const textoCentral = {
    id: 'textoCentral',
    beforeDraw(chart, args, options) {
        const { width, height } = chart;
        const ctx = chart.ctx;
        ctx.restore();
        ctx.font = 'bold 20px sans-serif';
        ctx.fillStyle = '#333';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        const total = options.total;
        ctx.fillText(`R$ ${total.toFixed(2)}`, width / 2, height / 2);
        ctx.save();
    }
};
